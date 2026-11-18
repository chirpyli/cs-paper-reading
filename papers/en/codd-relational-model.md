---
title: "The Birth of the Relational Model"
paperTitle: "A Relational Model of Data for Large Shared Data Banks"
authors:
  - "E. F. Codd"
year: 1970
venue: "Communications of the ACM"
paperUrl: "/papers/Codd_1970_A_relational_model.pdf"
description: "Codd's relational model transformed the paradigm of data management — from navigational access to declarative queries"
lang: en
tags:
  - relational-model
  - sql
topic: classic
difficulty: introductory
featured: true
---

## TL;DR

E. F. Codd's 1970 paper introduced the **relational data model**, representing data as mathematical n-ary relations and using first-order predicate logic as the foundation for query languages. This paper fundamentally changed the database field — data management shifted from "tell the computer *how* to find data" to "tell the computer *what* data you want."

## 1. Background & Motivation

### The Database Landscape of the Late 1960s

Before Codd's paper, database systems relied primarily on two models:

- **Hierarchical Model**: such as IBM's IMS, organizing data in tree structures
- **Network Model**: such as the CODASYL standard, organizing data in graph structures

The common problem with both models: **extremely poor data independence**. Programmers had to understand physical storage details, and query logic was tightly coupled with data access paths.

### Codd's Core Insight

While working at IBM's San Jose Research Laboratory, Codd identified three critical pain points:

1. **Ordering Dependence**: Changes in the physical ordering of data could break applications
2. **Indexing Dependence**: Adding or removing indexes could affect program correctness
3. **Access Path Dependence**: Programmers had to explicitly specify how to traverse data

Codd's solution: **abstract data as mathematical relations, and let the system — not the programmer — determine access paths**.

## 2. Core Ideas

### 2.1 Relation as the Data Model

Codd unified all data with a single elegant concept: **all data can be represented as n-ary relations (tables)**.

A relation R is a subset of the Cartesian product S₁ × S₂ × ... × Sₙ, where each Sᵢ is a domain. Intuitively, this is a table with rows and columns.

**Key abstractions**:
- There is no implicit ordering among the rows of a relation
- Columns are identified by attribute names, not positions
- Each cell value is atomic (First Normal Form)

### 2.2 Data Independence

One of the paper's most important contributions is the clear definition of two types of data independence:

- **Logical Data Independence**: New columns or relations can be added without affecting existing queries
- **Physical Data Independence**: Storage structures and indexes can be changed without modifying queries

### 2.3 Relational Algebra & Relational Calculus

The paper proposed two equivalent query languages:

- **Relational Algebra**: A set of operation primitives (selection, projection, join, union, difference, Cartesian product)
- **Relational Calculus**: A declarative language based on first-order predicate logic: `{ x | P(x) }`

These two formalisms laid the theoretical foundation for SQL.

## 3. Impact on Industry

### Direct Legacy

- **System R (IBM, 1974-1979)**: The first SQL implementation, validating the industrial feasibility of the relational model
- **Ingres (UC Berkeley, 1974-1980)**: Influenced PostgreSQL's design
- **Oracle (1979)**: The first commercial relational database

### Adoption in Modern Systems

Virtually all mainstream databases today are based on the relational model or its extensions:

| System      | Relationship to the Relational Model   |
|-------------|----------------------------------------|
| PostgreSQL  | Relational model + object extensions   |
| MySQL       | Pure relational model                  |
| SQLite      | Embedded relational model              |
| DuckDB      | Columnar relational, relational algebra optimizer |

### Limitations

Codd's relational model also faces challenges:

- **Impedance Mismatch**: The gap between the relational model and object-oriented programming languages gave rise to ORMs
- **Schema Rigidity**: This spurred the NoSQL movement (though relational databases have adapted via JSON/JSONB support)
- **Distributed Scaling**: Strict ACID guarantees are expensive in distributed environments, but NewSQL systems are bridging the gap

## 4. Further Reading

- [Codd's 1981 Turing Award Lecture](https://amturing.acm.org/award_winners/codd_1000892.cfm): Revisiting the birth of the relational concept
- [Chamberlin & Boyce (1974): SEQUEL — the precursor to SQL](https://doi.org/10.1145/800296.811515)
- [Why SQL Exists](/en/blog/why-sql-exists/): A blog post on SQL's design philosophy
- [RedBook](http://www.redbook.io/) Chapter 1: Relational Model Revisited
