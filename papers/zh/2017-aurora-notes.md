---
title: "Aurora 核心机制阅读札记"
slug: aurora-notes
paperTitle: "Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases"
authors:
  - "Alexandre Verbitski 等"
year: 2017
venue: "阅读札记"
paperUrl: "/papers/amazon-aurora-design-considerations-for-high-throughput-cloud-native-relational-databases.pdf"
paperUrlZh: "/papers/zh/aurora-notes/index.html"
description: "围绕 VDL/CPL、mini-transaction 与存储层日志回放，梳理 Aurora 共享存储的一致性设计要点"
lang: zh
tags:
  - aurora
  - reading-notes
  - consistency
topic: cloud-native
difficulty: advanced
featured: false
rating: 3
---

## 云原生数据库核心点

共享存储的实现方式，aurora通过复制来保证持久性，可靠性，通过多数派quorum来达成一致,存储节点之间通过gossip协议保证一致性。

log is database， 计算节点仅写WAL到存储，计算节点是无状态的。

存储层实现日志回放

需要处理主节点和从节点不一致的问题，从节点往往落后于主节点，需要保证线性一致性，即不能读到旧数据，需要保证读到的是比目前更新的数据，同时也要保证从节点请求的页回放时指定的LSN必须是完整的事务LSN结束点，不能读到事务的中间状态。即：

Replica在应用日志记录时遵循以下两条重要规则：
(a) 只有LSN小于或等于VDL的日志记录才会被应用
(b) 属于单个mini-transaction的日志记录在Replica的缓存中原子地应用，确保 Replica 看到所有数据库对象的一致性视图。

日志回放被下推到存储层，在那里可以在后台或按需生成数据库页面。 当然，从头开始从完整的修改链生成每个页面是极其昂贵的。因此，我们持续在后台物化数据库页面，避免每次需要时都从零重新生成。注意，后台物化从正确性的角度来看完全是可选的：对引擎而言，日志就是数据库，存储系统物化的任何页面只是日志应用的缓存。还要注意，与 checkpoint 不同，只有具有长修改链的页面才需要重新物化。Checkpoint由整个redo日志链的长度决定，而Aurora的页面物化由给定页面的链长度决定。
可以避免在需要时进行长时间的回放，提前进行一定的回放物化页面。


存储服务确定其可以保证所有先前日志记录可用的最高LSN（这被称为VCL或Volume Complete LSN）。 在存储恢复期间，所有LSN大于VCL的日志记录必须被截断。 然而，数据库可以通过标记日志记录并将其标识为CPL（Consistency Point LSN）来进一步约束允许截断的点子集。因此，我们定义 VDL（Volume Durable LSN）为小于或等于 VCL 的最高 CPL，并截断所有 LSN 大于 VDL 的日志记录。例如，即使我们拥有直到 LSN 1007 的完整数据，数据库可能只声明 900、1000 和 1100 是 CPL，此时我们必须在 1000 处截断。我们到 1007 是完整的，但只持久到 1000。

完整性和持久性因此是不同的，CPL 可以被认为是划分了某种必须按顺序接受的有限形式的存储系统事务。如果客户端不需要这种区分，它可以简单地将每条日志记录标记为 CPL。在实践中，数据库与存储的交互如下：
- 每个数据库级事务被分解为多个 mini-transaction (MTR)，它们有序且必须原子执行。
- 每个 mini-transaction 由多个连续的日志记录组成（数量根据需要）。
- mini-transaction 中的最后一条日志记录是 CPL。

在恢复时，数据库与存储服务通信以确定每个 PG 的持久点，使用它来建立 VDL，然后发出命令截断 VDL 之上的日志记录。

这一段比较重要，尤其是最后一条，需要保证数据库从节点回放日志时，replica看到所有数据库对象的一致性视图。
