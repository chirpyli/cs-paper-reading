---
title: "Raft 共识算法（学习笔记）"
slug: raft-notes
paperTitle: "In Search of an Understandable Consensus Algorithm"
authors:
  - "Diego Ongaro"
  - "John Ousterhout"
year: 2014
venue: "USENIX Annual Technical Conference (ATC)"
paperUrl: "/papers/raft.pdf"
description: "Raft 共识算法中文学习笔记：从 Leader 选举、日志复制、安全性出发，深入剖析日志不一致、旧任期提交、网络分区、成员变更、日志压缩与 Client Protocol 等工程实现问题"
paperUrlZh: "/papers/zh/raft-notes/index.html"
lang: zh
tags:
  - raft
  - consensus
  - distributed-systems
  - replicated-log
  - leader-election
topic: distributed-systems
difficulty: intermediate
featured: false
rating: 4
draft: false
---

Raft 共识算法在分布式系统中是常用的共识算法之一，论文原文 [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)。作者在论文中指出 Paxos 共识算法的两大问题：其一是难懂，其二是应用到实际系统存在困难。针对 Paxos 存在的问题，作者的目的是提出一个易懂的共识算法，论文中有单独一小节论述 Raft 是一个实用的、安全可用、有效易懂的共识算法。本文描述了 Raft 共识算法的细节，很多内容描述及引用图片均摘自论文原文。

> 本篇是同类笔记「Raft：寻找一种易于理解的共识算法」的**学习笔记版**，侧重 Raft 各机制细节与工程实现中各种异常情况的处理；若需要论文逐节全文翻译，请参阅另一篇。

## Raft 概述

我们主要分以下三部分对 Raft 进行讨论：

- Leader election——a new leader must be chosen when an existing leader fails.（领导人选举）
- Log replication——the leader must accept log entries from clients and replicate them across the cluster, forcing the other logs to agree with its own.（日志复制）
- Safety——the key safety property for Raft.（安全性）

正常工作过程中，Raft 分为两部分，首先是 leader 选举过程，然后在选举出来的 leader 基础上进行正常操作，比如日志复制操作等。

一个 Raft 集群通常包含 $2N+1$ 个服务器，允许系统有 $N$ 个故障服务器。每个服务器处于 3 个状态之一：`leader`、`follower` 或 `candidate`。正常操作状态下，仅有一个 leader，其他的服务器均为 follower。follower 是被动的，不会对自身发出的请求而是对来自 leader 和 candidate 的请求做出响应。leader 处理所有的 client 请求（若 client 联系 follower，则该 follower 将转发给 leader）。candidate 状态用来选举 leader。状态转换如下图所示：

![Raft 节点状态转换](../assets/raft/raft_leader_election.png)

为了进行领导人选举和日志复制等，需要服务器节点存储如下状态信息：

| 状态 | 所有服务器上持久存在的 |
| --- | --- |
| currentTerm | 服务器最后一次知道的任期号（初始化为 0，持续递增）|
| votedFor | 在当前获得选票的候选人的 Id |
| log[] | 日志条目集；每一个条目包含一个用户状态机执行的指令，和收到时的任期号 |

| 状态 | 所有服务器上经常变的 |
| --- | --- |
| commitIndex | 已知的最大的已经被提交的日志条目的索引值 |
| lastApplied | 最后被应用到状态机的日志条目索引值（初始化为 0，持续递增） |

| 状态 | 在领导人里经常改变的（选举后重新初始化） |
| --- | --- |
| nextIndex[] | 对于每一个服务器，需要发送给他的下一个日志条目的索引值（初始化为领导人最后索引值加一） |
| matchIndex[] | 对于每一个服务器，已经复制给他的日志的最高索引值 |

Raft 在任何时刻都满足如下特性：

- Election Safety：在一个任期中只能有一个 leader；
- Leader Append-Only：leader 不会覆盖或删除日志中的 entry，只有添加 entry（follower 存在依据 leader 回滚日志的情况）；
- Log Matching：如果两个日志包含了一条具有相同 index 和 term 的 entry，那么这两个日志在这个 index 之前的所有 entry 都相同；（可以思考一下这个是怎么保证的呢？由后面讲到的一致性检查来保证，即 follower 节点接收到日志复制请求后要进行一致性检查，其证明过程有点类似于数学归纳法）
- ++Leader Completeness：如果在某一任期一条 entry 被提交 committed 了，那么在更高任期的 leader 中这条 entry 一定存在；++ （领导人选举时会保证这一性质，后面会讲到这个问题）
- State Machine Safety：如果一个节点将一条 entry 应用到状态机中，那么任何节点也不会再次将该 index 的 entry 应用到状态机里；

下面我们详细讨论这几部分。

## Leader 选举

一个节点初始状态为 follower，当 follower 在选举超时时间内未收到 leader 的心跳消息，则转换为 candidate 状态。为了避免选举冲突，这个超时时间是一个随机数（一般为 150~300ms）。超时成为 candidate 后，向其他节点发出 `RequestVote` RPC 请求，假设有 $2N+1$ 个节点，收到 $N+1$ 个节点以上的同意回应，即被选举为 leader 节点，开始下一阶段的工作。如果在选举期间接收到 leader 发来的心跳信息，则 candidate 转为 follower 状态。

> 在选举期间，可能会出现多个 candidate 的情况，可能在一轮选举过程中都没有收到多数的同意票，此时再次随机超时，进入第二轮选举过程，直至选出 leader 或者重新收到 leader 心跳信息，转为 follower 状态。

正常状态下，leader 会不断的广播心跳信息，follower 收到 leader 的心跳信息后会重置超时。当 leader 崩溃或者出现异常离线，此时网络中 follower 节点接收不到心跳信息，超时再次进入选举流程，选举出一个 leader。

> 这里还有补充一些细节，每个 leader 可以理解为都是有自己的任期（term）的，每一期起始于选举阶段，直到因节点失效等原因任期结束。每一期选举期间，每个 follower 节点只能投票一次。图中 `t3` 可能是因为没有获得超半数票等造成选举失败，须进行下一轮选举，此时 follower 可以再次对最先到达的 candidate 发出的 `RequestVote` 请求投票（先到先得）。

![Raft 任期](../assets/raft/raft_term.png)

对所有的请求（RequestVote、AppendEntry 等请求），如果发现其 Term 小于当前节点，则拒绝请求；如果是 candidate 选举期间，收到不小于当前节点任期的 leader 节点发来的 `AppendEntry` 请求，则认可该 leader，candidate 转换为 follower。这里还有一些细节：follower 节点怎么判断我是否投票给 candidate 节点呢？或者说，选举领导人应该有怎样的原则呢？如何选举才能保证满足上面提到过的第 4 条性质？后面会讲到这个问题。

## 日志复制（Log replication）

前面 leader 选举的过程，leader 选举成功后，将进入有效工作阶段，即日志复制阶段，其中日志复制过程会分记录日志和提交数据两个阶段。

整个过程如下：

1. 首先 client 向 leader 发出 command 指令；（每一次 command 指令都可以认为是一个 entry，或者说是日志项）
2. leader 收到 client 的 command 指令后，将这个 command entry 追加到本地日志中，此时这个 command 是 uncommitted 状态，因此并没有更新节点的当前状态；
3. 之后，leader 向所有 follower 发送这条 entry，也就是通过日志复制 AppendEntries 消息 *（可以是一条也可以是多条日志项）* 将日志项复制到集群其他节点上，follower 接收到后 *（这里有判断条件的，并不是所有 leader 发送来的日志项都无条件接收，而且还可能存在本地与 leader 日志不一致的情况，后面会详细说明，这里先看正常情况）* 追加到本地日志中，并回应 leader 成功或者失败；
4. leader 收到大多数 follower 的确认回应后，此 entry 在 leader 节点由 uncommitted 变为 committed 状态，此时按这条 command 更新 leader 状态，或者说将该日志项应用到状态机，然后向 client 返回执行结果；
5. 在下一心跳中（这里也可以是或者说多数情况下是新的日志复制 AppendEntries 消息，会带有相关信息，后面会详细的字段说明会讲到），leader 会通知所有 follower 更新确认的 entry，follower 收到后，更新状态，这样，所有节点都完成 client 指定 command 的状态更新。

可以看到 client 每次提交 command 指令，服务节点都先将该指令 entry 追加记录到日志中，等 leader 确认大多数节点已追加记录此条日志后，再进行提交确认，更新节点状态。如果还对这个过程有些模糊的话，可以参考 [Raft 动画演示](http://thesecretlivesofdata.com/raft/)，较为直观的演示了领导人选举及日志复制的过程。这里讲到的都是正常情况下的运行过程。

实际上，还有很多问题需要考虑：follower 与 leader 日志不匹配或者不一致时怎么办？旧的 leader 挂掉了之后，新的 leader 怎么处理？成员怎么变更，或者说怎么添加成员？出现网络分区时会发生什么？网络分区恢复后，怎么处理状态不一致的情况？具体工程实现时，日志可能会面临无限增长的情况，有什么解决办法呢？我们下面就分析一下 raft 是怎么解决这些问题的。

## 安全（Safety）

前面描述了 Raft 算法是如何选举和复制日志的。然而，到目前为止描述的机制并不能充分的保证每一个状态机会按照相同的顺序执行相同的指令。我们需要再继续深入思考以下几个问题：

- 第一个问题，leader 选举时 follower 收到 candidate 发起的投票请求，如果同意就进行回应，但具体的规则是什么呢？是所有的 follower 都有可能被选举为领导人吗？
- 第二个问题，leader 可能在任何时刻挂掉，新任期的 leader 怎么提交之前任期的日志条目呢？

### 选举限制

针对第一个问题，之前并没有细讲。如果当前 leader 节点挂了，需要重新选举一个新 leader，此时 follower 节点的状态可能是不同的：有的 follower 可能状态与刚刚挂掉的 leader 相同，状态较新，有的 follower 可能记录的当前 index 比原 leader 节点的少很多，状态更新相对滞后。此时，从系统最优的角度看，选状态最新的 candidate 为佳；从正确性的角度看，要确保 Leader Completeness，即如果在某一任期一条 entry 被提交成功了，那么在更高任期的 leader 中这条 entry 一定存在。反过来讲就是如果一个 candidate 的状态旧于目前被 committed 的状态，它一定不能被选为 leader。具体到投票规则：

1）节点只投给拥有不比自己日志状态旧的节点；
2）每个节点在一个 term 内只能投一次，在满足 1 的条件下，先到先得；

我们看一下**请求投票 RPC**（由候选人负责调用用来征集选票）的定义：

| 参数 | 解释 |
| --- | --- |
| term | 候选人的任期号 |
| candidateId | 请求选票的候选人的 Id |
| lastLogIndex | 候选人的最后日志条目的索引值 |
| lastLogTerm | 候选人最后日志条目的任期号 |

| 返回值 | 解释 |
| --- | --- |
| term | 当前任期号，以便于候选人去更新自己的任期号 |
| voteGranted | 候选人赢得了此张选票时为真 |

接收者实现：

1. 如果 `term < currentTerm` 返回 false
2. 如果 votedFor 为空或者为 candidateId，并且候选人的日志至少和自己一样新，那么就投票给他

可以看到 RequestVote 投票请求中包含了 lastLogIndex 和 lastLogTerm 用于比较日志状态。这样，虽然不能保证最新状态的 candidate 成为 leader，但能够保证被选为 leader 的节点一定拥有最新被 committed 的状态，但不能保证拥有最新 uncommitted 状态 entries。

### 提交之前任期的日志条目

领导人知道一条当前任期内的日志记录是可以被提交的，只要它被存储到了大多数的服务器上。但是之前任期的未提交的日志条目，即使已经被存储到大多数节点上，也依然有可能会被后续任期的领导人覆盖掉。下图说明了这种情况：

![旧任期日志条目提交问题](../assets/raft/raft_log_entries.png)

> 如图的时间序列展示了为什么领导人无法决定对老任期号的日志条目进行提交。在 (a) 中，S1 是领导者，部分的复制了索引位置 2 的日志条目。在 (b) 中，S1 崩溃了，然后 S5 在任期 3 里通过 S3、S4 和自己的选票赢得选举，然后从客户端接收了一条不一样的日志条目放在了索引 2 处。然后到 (c)，S5 又崩溃了；S1 重新启动，选举成功，开始复制日志。在这时，来自任期 2 的那条日志已经被复制到了集群中的大多数机器上，但是还没有被提交。如果 S1 在 (d) 中又崩溃了，S5 可以重新被选举成功（通过来自 S2，S3 和 S4 的选票），然后覆盖了他们在索引 2 处的日志。反之，如果在崩溃之前，S1 把自己主导的新任期里产生的日志条目复制到了大多数机器上，就如 (e) 中那样，那么在后面任期里面这些新的日志条目就会被提交（因为 S5 就不可能选举成功）。这样在同一时刻就同时保证了，之前的所有老的日志条目就会被提交。

为了消除上图里描述的情况，Raft 永远不会通过计算副本数目的方式去提交一个之前任期内的日志条目。只有领导人当前任期里的日志条目通过计算副本数目可以被提交；一旦当前任期的日志条目以这种方式被提交，那么由于日志匹配特性，之前的日志条目也都会被间接的提交。

> 当领导人复制之前任期里的日志时，Raft 会为所有日志保留原始的任期号。

## 对 Raft 中几种情况的思考

### follower 节点与 leader 日志内容不一致时怎么处理？

![follower 与 leader 日志不一致](../assets/raft/raft_log_inconsistency.png)

我们先举例说明：正常情况下，follower 节点应该像 B 节点一样与 leader 节点日志内容一致，但也会出现 A、C 等情况，出现了不一致。以 A、B 节点为例，当 leader 节点向 follower 节点发送 AppendEntries `<prevLogIndex=7, prevLogTerm=3, entries=[x<-4]>, leaderCommit=7` 时，我们分析一下发生了什么：B 节点日志与 `prevLogIndex=7, prevLogTerm=3` 相匹配，将 `index=7`（`x<-5`）这条 entry 提交 committed，并在日志中新加入 entry `x<-4`，处于 uncommitted 状态；A 节点接收到时，当前日志 `index < prevLogIndex` 与 `prevLogIndex=7, prevLogTerm=3` 不相匹配，拒绝该请求返回 false，不会将 `x<-4` 添加到日志中。当 leader 知道 A 节点因日志不一致拒绝了该请求后，不断递减 `prevLogIndex` 重新发送请求，直到 A 节点 `index, term` 与 `prevLogIndex, prevLogTerm` 相匹配，将 leader 的 entries 复制到 A 节点中，达成日志状态一致。

我们看一下**附加日志 AppendEntries RPC**（由领导人负责调用复制日志指令；也会用作 heartbeat）的定义：

| 参数 | 解释 |
| --- | --- |
| term | 领导人的任期号 |
| leaderId | 领导人的 Id，以便于跟随者重定向请求 |
| prevLogIndex | 新的日志条目紧随之前的索引值 |
| prevLogTerm | prevLogIndex 条目的任期号 |
| entries[] | 准备存储的日志条目（表示心跳时为空；一次性发送多个是为了提高效率） |
| leaderCommit | 领导人已经提交的日志的索引值 |

| 返回值 | 解释 |
| --- | --- |
| term | 当前的任期号，用于领导人去更新自己 |
| success | 跟随者包含了匹配上 prevLogIndex 和 prevLogTerm 的日志时为真 |

接收者实现：

1. 如果 `term < currentTerm` 就返回 false；
2. 如果日志在 prevLogIndex 位置处的日志条目的任期号和 prevLogTerm 不匹配，则返回 false；
3. 如果已经存在的日志条目和新的产生冲突（索引值相同但是任期号不同），删除这一条和之后所有的；（raft 中 follower 处理不一致的一个原则就是一切听从 leader）
4. 附加日志中尚未存在的任何新条目；
5. 如果 `leaderCommit > commitIndex`，令 commitIndex 等于 leaderCommit 和新日志条目索引值中较小的一个；

简单总结一下，出现不一致时核心的处理原则是一切遵从 leader。当 leader 向 follower 发送 AppendEntry 请求，follower 对 AppendEntry 进行一致性检查，如果通过，则更新状态信息；如果发现不一致，则拒绝请求；leader 发现 follower 拒绝请求，出现了不一致，此时将递减 nextIndex，并重新给该 follower 节点发送日志复制请求，直到找到日志一致的地方为止。然后把 follower 节点的日志覆盖为 leader 节点的日志内容。

### leader 挂掉了，怎么处理？

前面可能断断续续的提到这种情况的处理方法，首要的就是选出新 leader。选出新 leader 后，可能上一任期还有一些 entries 并没有提交，处于 uncommitted 状态，该怎么办呢？处理方法是新 leader 只处理提交新任期的 entries。上一任期未提交的 entries，如果在新 leader 选举前已经被大多数节点记录在日志中，则新 leader 在提交最新 entry 时，之前处于未提交状态的 entries 也被 committed 了，因为如果两个日志包含了一条具有相同 index 和 term 的 entry，那么这两个日志在这个 index 之前的所有 entry 都相同；如果在新 leader 选举前没有被大多数节点记录在日志中，则原有未提交的 entries 有可能被新 leader 的 entries 覆盖掉，这个问题前面已经讲过。

### 出现网络分区时怎么处理？

分布式系统中网络分区的情况基本无法避免。出现网络分区时，原有 leader 在分区的一侧，此时如果客户端发来指令，旧 leader 依旧在分区一侧进行日志复制的过程，但因收不到大多数节点的确认，客户端所提交的指令 entry 只能记录在日志中，无法进行提交确认，处于 uncommitted 状态。而在分区的另一侧，此时收不到心跳信息，会进入选举流程重新选举一个 leader，新 leader 负责分区另一侧的请求，进行日志复制等操作。因为新 leader 可以收到大多数 follower 确认，客户端的指令 entry 可以被提交，并更新节点状态。当网络分区恢复时，此时两个 `leader` 会收到彼此广播的心跳信息，旧 leader 发现更大 term 的 leader，转为 follower，此时旧 leader 分区一侧的所有操作都要回滚，接受新 leader 的更新。

### 成员变更问题，如何添加成员？

在分布式系统中，节点数量或者说服务器数量不是一成不变的，我们有可能会随时增减节点数量。当增加节点时，有可能会出现两个 leader 选举成功的情况，主要是新旧配置不一致造成的，怎么处理呢？最简单粗暴的就是把目前所有节点都停掉，更新配置，再重启所有节点，但会造成一段时间服务不可用，很多情况下这是不能被允许的。raft 的解决办法原论文中是联合共识（Joint Consensus）的办法，后来又提出了单节点变更（single-server changes）的方法。我们下面详细描述一下这个问题。

Raft 要求，在任一任期内，只能有一个 leader，而成员变更的麻烦就在于，成员变更时可能会出现两个 leader。以一个例子说明：原系统有 3 个节点，成员为 [1,2,3]，现新增成员 **4、5**。假设在成员变更时，1、2 与 3 发生分区，此时 [1,2] 为一组，1 通过 1、2 两节点选举为 leader，而 5 通过 3、4、5 选举为 leader，就形成了 2 个 leader 并存的情况。

![成员变更导致双 leader](../assets/raft/raft_member_change.png)

因为每个节点新旧配置更新的时间不同，造成了在某一时刻，可能会存在新旧配置的两个大多数情况的存在。上图中，旧配置的大多数是两个节点，而新配置的大多数是三个节点，在图中红线头的时刻存在两个大多数的情况，如果此时出现网络分区进行选举时就会出现两个 leader 的情况。

怎么解决呢？用什么办法才能不让上面两个大多数情况的出现呢？可通过单节点变更解决，即通过一次变更一个节点实现成员变更。主要思想是利用"一次变更一个节点，不会同时存在旧配置和新配置的两个大多数"的特性，实现成员变更。比如上面的情况，就可先将 3 节点集群 [A,B,C] 变更为 4 节点集群 [A,B,C,D]，再将 4 节点集群变更为 5 节点集群 [A,B,C,D,E]。

> 为什么单节点变更不会造成两个大多数情况的出现呢？我们可以进行如下推理：假设原节点数为 `2n+1`，则旧配置的大多数 `major_old = n+1`，新加入 1 个节点，新配置节点数为 `2n+2`，则新配置的大多数为 `major_new = n+2`，同时存在两个大多数所需节点数目为 `major = major_old + major_new = n+1 + n+2 = 2n+3 > 2n+2`，也就是两个大多数所需节点数超出了节点总数，故不存在这种情况。如何是删除成员，其推理过程类似，结论相同。

具体的，我们依旧以这个 3 节点集群变更为 5 节点集群为例进行说明。假设现 3 节点集群 [<font color=red>A</font>, B, C]，节点 A 为 leader，配置为 [A,B,C]，我们先向集群加入节点 D，新的配置为 [A,B,C,D]，成员变更通过以下两步实现：

- 第一步，leader 节点 A 向新节点 D 同步数据；
- 第二步，leader 将新配置 [A,B,C,D] 作为一个日志项复制到新配置中的所有节点（A,B,C,D）上，然后将新配置的日志项应用到本地状态机，完成单节点变更。

在变更后，现有集群的配置项就是 [A,B,C,D]，添加 E 节点也是同样的步骤。上面的描述如果理解的比较模糊的话，其实 raft 是采用将修改集群配置的命令放在日志条目中来处理的，其修改配置项，就是一条日志项，其流程与普通的日志项相同，只不过最后状态机执行的结果是配置变更。

## 日志压缩

日志压缩主要是为了解决无限增长的日志与有限的存贮空间的矛盾。可以想一个问题：对于已经 committed 的日志项，是否有必要一直保存下去？如果没有必要的话，是否可以对部分已 committed 的日志项删减或压缩呢？raft 的主要的解决办法是采用快照进行日志压缩。

![日志压缩快照](../assets/raft/raft_snap.png)

如上图所示，对于日志索引 5 之前的日志项可以删除，只保留一个快照（保存有当前状态以及一些任期索引号等元信息）即可。

具体工程实现时，一般每个节点独立打快照，当日志超过一定量会触发快照操作，具体实现以及更多细节待以后深究。

## Client Protocol

raft 共识算法真正工作时还需有一个客户端协议（client protocol），综合解决一些列的问题。比如会遇到下面这些问题：client 怎么和集群交互呢？client 如果知道 leader 节点的话，可以直接将 command 发给 leader 节点；如果不知道的话，可以随意发给集群中已知的节点，节点会将 client 的请求转给 leader。其实上面还有个问题，client 发送请求（或者 command）给 leader，但是 leader 迟迟不给回应怎么办？重试是一个办法。连接的 leader 崩溃了 client 怎么办？如果 client 超时重发 command，怎么保证 command 不被状态机执行两次？client 生成 command 的时候要给加上唯一 ID，当 server 的日志中已存在相同 command 时会忽略。

## 附录

这里附加一张论文中的截图，里面详细讲明了不同节点需要维护什么信息，每个消息是怎么定义的，以及消息该如何处理等，不包含日志压缩以及成员变更部分：

![Raft 算法总结](../assets/raft/raft_summary.png)

这里补充一点，raft 共识算法与 pbft 共识算法解决的是不同的问题，即 raft 节点不能存在恶意节点，节点消息可以延迟、丢失，但不能造假或作恶，即不能存在拜占庭节点。

本文对 raft 共识算法做了一个整体的梳理学习，可能会存在某些细节描述不清晰的地方，在真正工程代码实现时，还会存在更多的细节问题。同时，这里缺少证明为什么 raft 算法是正确的证明，有待今后更深一步理解共识算法后再行补充。

---

> 参考文档：
> [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)
> [raft 论文中文翻译](https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md)
