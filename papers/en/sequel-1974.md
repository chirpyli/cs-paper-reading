---
title: "The Precursor to SQL: The Birth of SEQUEL"
paperTitle: "SEQUEL: A Structured English Query Language"
authors:
  - "Donald D. Chamberlin"
  - "Raymond F. Boyce"
year: 1974
venue: "Proceedings of the 1974 ACM SIGFIDET Workshop"
paperUrl: "/papers/2705-sequel-1974.pdf"
paperUrlZh: "/papers/zh/sequel-1974/index.html"
description: "Chamberlin and Boyce proposed the Structured English Query Language SEQUEL, replacing predicate calculus with SELECT-FROM-WHERE blocks — the direct ancestor of SQL"
lang: en
tags:
  - sql
  - sequel
  - query-language
topic: optional
difficulty: introductory
featured: true
---

## TL;DR

In 1974, Chamberlin and Boyce proposed SEQUEL (Structured English Query Language) — later renamed SQL for trademark reasons. SEQUEL was designed to give non-programmers (accountants, engineers, architects, urban planners) an English-like way to query databases, replacing the complex quantifiers and bound variables of predicate calculus with a simple SELECT-FROM-WHERE block template.

## 1. Background & Motivation

### From SQUARE to SEQUEL

SEQUEL's predecessor was the SQUARE language, developed by Boyce and Chamberlin in 1973. SQUARE had successfully eliminated quantifiers and explicit linking terms from predicate calculus, but its concise mathematical notation still presented too high a barrier for ordinary users.

SEQUEL's key design shifts:
- **Mathematical notation → English keywords**: replaced SQUARE's superscript/subscript mapping notation with `SELECT ... FROM ... WHERE`
- **Top-down structured programming**: queries organized as nested blocks, supporting progressive construction
- **Linear notation**: queries read left-to-right and top-to-bottom, matching natural reading habits

### Target Audience

The paper explicitly positions SEQUEL for "knowledge workers who are not computer specialists" — accountants, engineers, architects, and urban planners. This design philosophy profoundly shaped SQL's core character as a declarative, natural-language-like language.

## 2. Core Ideas

### 2.1 The SELECT-FROM-WHERE Template

SEQUEL's most fundamental innovation is the three-component template:

```
SELECT   the columns you want
FROM     the table containing the data
WHERE    the filter conditions on rows
```

This template mirrors the natural way people use tables — "from some table, select certain columns, when rows satisfy certain conditions." The paper notes that in an interactive system, "this template might be presented to the user, who then fills in the blanks." This design gave SEQUEL an extremely low learning curve.

### 2.2 Mapping as the Query Primitive

SEQUEL models queries as "mapping" operations:
- Each SELECT-FROM-WHERE block defines a mapping from a table to a result set
- Mappings can be arbitrarily nested — the output of an inner mapping serves as the matching condition for the outer mapping
- Mapping results are sets of values, supporting set operations (union, intersection, difference)

This follows directly from Codd's relational algebra closure property: the input and output of every mapping is a set, enabling arbitrary composition.

### 2.3 The Introduction of GROUP BY

This paper introduced the GROUP BY clause for the first time, addressing the common query pattern of "grouping table rows by column values before performing aggregation."

**Key insight**: In SQUARE, such "grouping" queries required introducing free variables (e.g., `x: EMP`), while SEQUEL elegantly eliminated the need for free variables through the GROUP BY syntactic sugar.

```sql
-- SQUARE (requires free variables)
x: EMP : COUNT( EMP(x.MGR = x.NAME) ) > 10

-- SEQUEL (GROUP BY eliminates free variables)
SELECT MGR
FROM EMP GROUP BY MGR
WHERE COUNT(NAME) > 10
```

### 2.4 Block Labels and Self-Referencing Queries

SEQUEL allows attaching labels to mapping blocks (e.g., `B1:`) to resolve column ambiguity in self-referencing queries — for example, "find employees whose salary exceeds their manager's salary," which requires correlating different rows of the same table. This feature was later inherited by SQL's **correlation name** (table alias) mechanism.

### 2.5 Structured Composition Rules

SEQUEL's core design philosophy: **reduce complex queries to a few basic building blocks + a simple set of composition rules**.

```
Building blocks = SELECT-FROM-WHERE mappings
Composition     = nesting | set operations | grouping | label references
```

This design was directly influenced by structured programming ideas (Dijkstra et al.). Its aesthetic value lies in the fact that users need only understand one pattern (SELECT-FROM-WHERE) and can then build arbitrarily complex queries by repeatedly applying composition rules.

## 3. Impact on Industry

### Direct Legacy

| Year | Event |
|------|-------|
| 1974 | Chamberlin & Boyce publish the SEQUEL paper |
| 1974–1979 | IBM System R implements SEQUEL/2 (later renamed SQL) |
| 1979 | Oracle V2 becomes the first commercial SQL implementation |
| 1986 | ANSI adopts SQL as a standard (SQL-86) |
| 1987 | ISO adopts SQL as an international standard |

### Design Differences: SEQUEL vs. SQL

Many of SEQUEL's design choices directly entered SQL, but some evolved:

| Feature | SEQUEL (1974) | SQL (Modern) |
|---------|---------------|--------------|
| Basic query block | SELECT-FROM-WHERE | SELECT-FROM-WHERE (identical) |
| Set operations | Supports ∩, ∪, − | Supports INTERSECT, UNION, EXCEPT |
| Aggregate functions | SUM, COUNT, AVG, MAX, MIN, SET | Added STDDEV, VARIANCE, etc. |
| GROUP BY | Present | Present (pioneered by SEQUEL) |
| HAVING | None (uses WHERE) | Independent HAVING clause |
| Block labels | `B1: SELECT ... WHERE ... = B1.MGR` | Table alias (correlation name) |
| ORDER BY | None | Present (added later) |

### Modern System Inheritance

- **All SQL databases** directly inherit SEQUEL's SELECT-FROM-WHERE paradigm
- **DuckDB**'s vectorized execution engine internally maps SQL to relational algebra operator trees, continuing SEQUEL's "mapping composition" ideas
- **GoogleSQL / BigQuery**, **Presto**, and other big data query engines still use the same syntactic template

## 4. Limitations

- **SEQUEL is a pure query language**: no DDL (data definition), no DCL (access control) — these were gradually added in System R
- **No ORDER BY**: the original paper had no sorting support; users had to handle result ordering themselves
- **Primitive GROUP BY semantics**: no HAVING clause (post-aggregation conditions were written directly with WHERE), corrected in later SQL standards
- **Naive string/number comparison**: wrapped in quotes (`'8000'`), lacking a modern type system

## 5. Further Reading

- [Codd (1970): The Relational Model](/en/papers/codd-relational-model/) — SEQUEL's theoretical foundation
- [Why SQL Exists](/en/blog/why-sql-relational-theory/) — the historical motivations behind relational database theory
- [System R Paper (1976)](https://doi.org/10.1145/320455.320457) — the first SQL implementation
- [Reading Notes on SQL and Relational Theory](/en/blog/sql-and-relational-theory/) — comparing SQL and the relational model
