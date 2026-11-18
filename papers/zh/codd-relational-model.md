---
title: "关系模型的诞生"
paperTitle: "A Relational Model of Data for Large Shared Data Banks"
authors:
  - "E. F. Codd"
year: 1970
venue: "Communications of the ACM"
paperUrl: "/papers/Codd_1970_A_relational_model.pdf"
paperUrlZh: "/papers/zh/codd-relational-model/index.html"
description: "Codd 提出的关系模型改变了数据管理的范式——从导航式访问到声明式查询"
pubDate: 2026-07-04
lang: zh
tags:
  - relational-model
  - sql
topic: classic
difficulty: introductory
featured: true
---

## TL;DR

E. F. Codd 在 1970 年发表的这篇论文提出了**关系数据模型**（Relational Model），用数学上的 n 元关系（n-ary relation）来统一表示数据，并用一阶谓词逻辑作为查询语言的基础。这篇论文彻底改变了数据库领域——从此数据管理从"告诉计算机怎么找数据"变成了"告诉计算机你要什么数据"。

## 1. 背景与动机

### 1960 年代末的数据库现状

在 Codd 发表这篇论文之前，数据库系统主要依赖两种模型：

- **层次模型**（Hierarchical Model）：如 IBM 的 IMS，数据组织为树形结构
- **网状模型**（Network Model）：如 CODASYL 标准，数据组织为图结构

这两种模型的共同问题：**数据独立性极差**。程序员必须了解数据的物理存储方式，查询逻辑与数据访问路径强耦合。

### Codd 的核心洞察

Codd 在 IBM San Jose 实验室工作期间，观察到三个关键痛点：

1. **排序依赖**（Ordering Dependence）：数据的物理顺序变化会导致应用程序需要修改
2. **索引依赖**（Indexing Dependence）：添加或删除索引会影响程序的正确性
3. **访问路径依赖**（Access Path Dependence）：程序员必须显式指定遍历数据的方式

Codd 的解决方案：**用数学关系（relation）抽象数据，让系统而非程序员决定访问路径**。

## 2. 核心思想

### 2.1 关系作为数据模型

Codd 用一个简单的思想统一了所有数据：**所有数据都可以表示为 n 元关系（表）**。

一个关系 R 是笛卡尔积 S₁ × S₂ × ... × Sₙ 的子集，其中每个 Sᵢ 是一个域（domain）。直观理解就是一张有行和列的表。

**关键抽象**：
- 关系的行之间没有隐含的顺序
- 列由属性名（非位置）标识
- 每个单元格的值是原子的（第一范式）

### 2.2 数据独立性

论文最重要的贡献之一是明确定义了两种数据独立性：

- **逻辑数据独立性**：可以在不影响已有查询的情况下添加新的列或关系
- **物理数据独立性**：可以改变存储结构、索引而无需修改查询

### 2.3 关系代数与关系演算

论文提出了两种等价的查询语言：

- **关系代数**（Relational Algebra）：一组操作原语（选择、投影、连接、并、差、笛卡尔积）
- **关系演算**（Relational Calculus）：基于一阶谓词逻辑的声明式语言 `{ x | P(x) }`

这两种语言奠定了 SQL 的理论基础。

## 3. 对工业界的影响

### 直接遗产

- **System R (IBM, 1974-1979)**：第一个 SQL 实现，验证了关系模型的工业可行性
- **Ingres (UC Berkeley, 1974-1980)**：影响了 PostgreSQL 的设计
- **Oracle (1979)**：第一个商业关系数据库

### 现代系统继承

至今，几乎所有主流数据库都基于关系模型或其扩展：

| 系统 | 与关系模型的关系 |
|------|-----------------|
| PostgreSQL | 关系模型 + 对象扩展 |
| MySQL | 纯关系模型 |
| SQLite | 嵌入式关系模型 |
| DuckDB | 列存关系模型，嵌入关系代数优化器 |

### 局限性

Codd 的关系模型也面临挑战：

- **阻抗不匹配**（Impedance Mismatch）：关系模型与面向对象编程语言之间的鸿沟催生了 ORM
- **Schema 刚性问题**：催生了 NoSQL 运动（但关系模型通过 JSON/JSONB 适应了这一挑战）
- **分布式扩展**：ACID 严格保证在分布式环境下成本高昂，但 NewSQL 在努力弥合

## 4. 延伸阅读

- [Codd 1981 年图灵奖演讲](https://amturing.acm.org/award_winners/codd_1000892.cfm)：回顾关系数据库的概念诞生
- [Chamberlin & Boyce (1974)：SEQUEL — SQL 的前身](https://doi.org/10.1145/800296.811515)
- [为什么会有 SQL](/zh/blog/why-sql-exists/)：本站关于 SQL 设计哲学的博文
- [RedBook](http://www.redbook.io/) 第 1 章：关系模型回顾
