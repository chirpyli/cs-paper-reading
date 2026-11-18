---
title: "System R：关系数据库管理的里程碑"
paperTitle: "System R: Relational Approach to Database Management"
authors:
  - "M. M. Astrahan"
  - "M. W. Blasgen"
  - "D. D. Chamberlin"
  - "K. P. Eswaran"
  - "J. N. Gray"
  - "P. P. Griffiths"
  - "W. F. King"
  - "R. A. Lorie"
  - "P. R. McJones"
  - "J. W. Mehl"
  - "G. R. Putzolu"
  - "I. L. Traiger"
  - "B. W. Wade"
  - "V. Watson"
year: 1976
venue: "ACM Transactions on Database Systems, Vol. 1, No. 2"
paperUrl: "/papers/system-r-relational-approach-to-database-management.pdf"
paperUrlZh: "/papers/zh/system-r-1976/index.html"
description: "IBM 圣何塞研究实验室的 System R 团队首次完整描述了关系数据库管理系统的架构与实现，涵盖优化器、视图、授权、并发控制、恢复等核心子系统"
lang: zh
tags:
  - system-r
  - relational-model
  - sql
  - database
topic: classic
difficulty: advanced
featured: true
rating: 5
---

## TL;DR

1976 年，IBM 圣何塞研究实验室的 14 位作者在 ACM TODS 上发表了 System R 的系统架构论文。这是关系数据库历史上最重要的工程论文之一：它第一次完整描述了一个真正可用的关系数据库管理系统是如何构建的——从外层的 SEQUEL 查询语言、游标接口、视图和授权，到内层的优化器、索引结构（B-tree）、指针链接、事务一致性级别、锁层次协议，再到系统级的检查点和崩溃恢复。

## 1. 背景与动机

Codd 在 1970 年提出关系模型时，回答的是"是什么"的问题。System R 项目则首次大规模地回答了"怎么做"的问题：一个完整的关系数据库系统能否在真实环境中实际运行，并有与当时主流系统（IMS、CODASYL）相比有竞争力的性能？

论文作者阵容堪称数据库领域的"梦之队"：Astrahan、Chamberlin（SEQUEL/SQL 的共同设计者）、Gray（事务处理的奠基人）、Lorie、Traiger 等。这篇论文奠定了此后几十年关系数据库系统设计的蓝图。

## 2. 核心贡献

### 2.1 两层架构：RDS + RSS

System R 首次明确地将数据库系统分为两层：
- **关系数据系统 (RDS)**：处理查询语言、视图、授权、完整性、优化器
- **关系存储系统 (RSS)**：处理存储、索引、事务、锁定、恢复

这种分层设计思想影响了几乎所有的后续数据库系统。

### 2.2 查询优化器

System R 的优化器是第一个基于代价的关系查询优化器。它的核心思想至今仍被使用：
- 基于统计信息（基数、页数等）估算每种执行方案的成本
- 成本度量基于磁盘页访问数（I/O）
- 对于多表连接，考虑多种执行策略（嵌套循环、排序合并、TID 算法）
- 生成"优化包"存储视图的预优化执行计划

### 2.3 SQL 的雏形：SEQUEL

论文详细描述了 SEQUEL 语言在这个系统中的实现：
- SELECT-FROM-WHERE 块结构
- GROUP BY 和 HAVING 的分离
- 支持 JOIN（FROM 子句多表 + WHERE 条件）
- 集合操作（UNION、INTERSECT、MINUS）
- 游标接口与宿主语言的绑定

### 2.4 事务与一致性

System R 首次定义了三级一致性模型（Level 1/2/3），这与后来的隔离级别（读未提交、读已提交、可序列化）一一对应。论文还描述了锁层次协议（意向锁）和死锁检测机制。

### 2.5 视图与授权

System R 将视图作为授权的核心机制，支持 GRANT/REVOKE，并提出视图更新的"一对一规则"。

### 2.6 存储与恢复

RSS 的设计极为精巧：基于页图的段恢复机制、影子页技术实现了高效的检查点与回滚、B-tree 索引结构和指针链（链接）提供了丰富的访问路径。

## 3. 为什么重要

这篇论文不仅是学术研究，更是工程实践的报告。它证明了关系模型不是象牙塔里的数学玩具，而是可以实际落地的工程系统。文中描述的优化器架构、事务管理、三级一致性、锁层次等技术概念，至今仍是关系数据库教科书的核心内容。

如果你想理解 PostgreSQL、MySQL、Oracle 等现代数据库的内部设计思想，这篇论文是最重要的源头文献之一。

## 4. 扩展阅读

- Codd (1970): 关系模型的理论基础
- Chamberlin & Boyce (1974): SEQUEL 语言的设计
- Gray et al. (1976): 锁的粒度与一致性级别（本文引用 [13]）
- Stonebraker et al. (1976): INGRES 系统——System R 的并行竞争者
