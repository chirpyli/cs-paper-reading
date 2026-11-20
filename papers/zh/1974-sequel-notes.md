---
title: "SQL 的前身：SEQUEL 的诞生（学习笔记）"
slug: sequel-notes
paperTitle: "SEQUEL: A Structured English Query Language"
authors:
  - "Donald D. Chamberlin"
  - "Raymond F. Boyce"
year: 1974
venue: "Proceedings of the 1974 ACM SIGFIDET Workshop"
paperUrl: "/papers/2705-sequel-1974.pdf"
paperUrlZh: "/papers/zh/sequel-notes/index.html"
description: "Chamberlin 和 Boyce 提出了结构化英语查询语言 SEQUEL，用 SELECT-FROM-WHERE 块取代了谓词演算，成为 SQL 的雏形"
lang: zh
tags:
  - sql
  - sequel
  - query-language
topic: optional
difficulty: introductory
featured: true
rating: 5
---

## TL;DR

Chamberlin 和 Boyce 在 1974 年提出了 SEQUEL（Structured English Query Language）——后来因商标原因改名为 SQL。SEQUEL 的设计目标是为非计算机专业用户（会计师、工程师、建筑师等）提供一种类英语的数据库查询方式，用 SELECT-FROM-WHERE 块的简单模板取代了基于谓词演算的语言中复杂的量词和约束变量。

## 1. 背景与动机

### 从 SQUARE 到 SEQUEL

SEQUEL 的前身是 Boyce 和 Chamberlin 在 1973 年开发的 SQUARE 语言。SQUARE 已经成功地消除了谓词演算中的量词和显式链接项，但其使用简洁的数学记法，对普通用户来说学习门槛仍然太高。

SEQUEL 的关键设计转变：
- **数学记法 → 英语关键词**：用 `SELECT ... FROM ... WHERE` 替代 SQUARE 中的上下标映射记法
- **自顶向下结构化编程**：查询以嵌套的块结构组织，支持渐进式构建
- **线性记法**：查询从左到右、从上到下阅读，符合自然阅读习惯

### 目标用户

论文明确将 SEQUEL 定位为面向"非计算机专家的知识工作者"——会计师、工程师、建筑师、城市规划师。这一设计哲学深刻影响了 SQL 至今"声明式、类自然语言"的核心特质。

## 2. 核心思想

### 2.1 SELECT-FROM-WHERE 模板

SEQUEL 最基础的创新是 SELECT-FROM-WHERE 三组件模板：

```
SELECT   要查询的列
FROM     数据所在表
WHERE    筛选条件
```

这个模板模拟了人们使用表格的自然方式——"从某张表中，选择某些列，当行满足某些条件时"。论文指出，在交互式系统中，"这个模板可以被呈现给用户，用户只需填空即可"。这种设计使 SEQUEL 具备了极低的学习门槛。

### 2.2 映射（Mapping）作为查询基元

SEQUEL 将查询建模为"映射"操作：
- 每个 SELECT-FROM-WHERE 块定义了一个从表到结果集的映射
- 映射可以任意嵌套——内部映射的输出作为外部映射的匹配条件
- 映射的结果是值集合，支持集合运算（并、交、差）

这与 Codd 关系代数的闭包性质一脉相承：每个映射的输入和输出都是集合，因此可以任意组合。

### 2.3 GROUP BY 的引入

论文首次提出了 GROUP BY 子句的概念，用于解决"需要将表中的行按某列值分组后再进行聚合操作"的常见查询模式。

**关键洞察**：在 SQUARE 中，这类"分组"查询需要引入自由变量（如 `x: EMP`），而 SEQUEL 用 `GROUP BY` 语法糖优雅地消除了自由变量的需要。

```sql
-- SQUARE（需要自由变量）
x: EMP : COUNT( EMP(x.MGR = x.NAME) ) > 10

-- SEQUEL（用 GROUP BY 消除自由变量）
SELECT MGR
FROM EMP GROUP BY MGR
WHERE COUNT(NAME) > 10
```

### 2.4 块标签与自引用查询

SEQUEL 允许为映射块附加标签（如 `B1:`），用于解决自引用查询中的列歧义——例如"查询薪水高于其经理的员工"这类需要将同一表的不同行进行关联的查询。这一特性在后来被 SQL 的**表别名**（correlation name）机制所继承。

### 2.5 结构化组合规则

SEQUEL 的核心设计哲学是：**将复杂查询简化为几个基本构建块 + 一套简单的组合规则**。

```
基本构建块 = SELECT-FROM-WHERE 映射
组合规则   = 嵌套 | 集合运算 | 分组 | 标签引用
```

这种设计受结构化编程思想（Dijkstra 等）的直接影响，其美学价值在于：用户只需要理解一个模式（SELECT-FROM-WHERE），就可以通过反复应用组合规则来构建任意复杂的查询。

## 3. 对工业界的影响

### 直接遗产

| 年份 | 事件 |
|------|------|
| 1974 | Chamberlin & Boyce 发表 SEQUEL 论文 |
| 1974–1979 | IBM System R 实现 SEQUEL/2（后改名 SQL） |
| 1979 | Oracle V2 成为首个商业 SQL 实现 |
| 1986 | ANSI 采纳 SQL 为标准（SQL-86） |
| 1987 | ISO 采纳 SQL 为国际标准 |

### SEQUEL 与 SQL 的设计差异

SEQUEL 的许多设计选择直接进入了 SQL，但也有一些演化和偏离：

| 特性 | SEQUEL (1974) | SQL (现代) |
|------|---------------|------------|
| 基本查询块 | SELECT-FROM-WHERE | SELECT-FROM-WHERE（与 SEQUEL 一致） |
| 集合运算 | 支持 ∩, ∪, − | 支持 INTERSECT, UNION, EXCEPT |
| 聚合函数 | SUM, COUNT, AVG, MAX, MIN, SET | 增加了标准差、方差等 |
| GROUP BY | 有 | 有（SEQUEL 首创） |
| HAVING | 无（用 WHERE 代替） | 独立 HAVING 子句 |
| 块标签 | `B1: SELECT ... WHERE ... = B1.MGR` | 表别名（correlation name） |
| ORDER BY | 无 | 有（后来加入） |

### 现代系统的继承

- **所有 SQL 数据库**直接继承 SEQUEL 的 SELECT-FROM-WHERE 范式
- **DuckDB** 的向量化执行引擎在内部将 SQL 映射为关系代数操作树，与 SEQUEL 的"映射组合"思想一脉相承
- **GoogleSQL / BigQuery**、**Presto** 等大数据查询引擎仍然使用相同的语法模板

## 4. 局限性

- **SEQUEL 是纯查询语言**：不包含 DDL（数据定义）、DCL（权限控制）等，这些在 System R 中才逐步加入
- **无 ORDER BY**：论文原版不支持排序，用户需要自行处理结果顺序
- **GROUP BY 语义较初代**：不支持 HAVING 子句（聚合后的条件直接用 WHERE 写），这在后续 SQL 标准中被纠正
- **字符串/数字比较的朴素处理**：用引号包裹（`'8000'`），缺乏现代 SQL 的类型系统

## 5. 延伸阅读
- [System R 论文 (1976)](https://scispace.com/pdf/system-r-relational-approach-to-database-management-12pgrxfjws.pdf) —— 第一个 SQL 实现
