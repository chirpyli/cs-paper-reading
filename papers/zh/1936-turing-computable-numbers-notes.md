---
title: "可计算数与通用机器：图灵 1936 年论文学习笔记"
slug: turing-computable-numbers-notes
paperTitle: "On Computable Numbers, with an Application to the Entscheidungsproblem"
authors:
  - "Alan M. Turing"
year: 1936
venue: "Proceedings of the London Mathematical Society"
paperUrl: "/papers/Turing_1936_On_Computable_Numbers.pdf"
paperUrlZh: "/papers/zh/turing-computable-numbers-notes/index.html"
description: "图灵 1936 年论文学习笔记：从纸带机器、描述数与通用机，到对角论证、停机类不可判定性、λ-可定义性与判定问题不可解"
lang: zh
tags:
  - computability
  - turing-machine
  - universal-machine
  - undecidability
  - entscheidungsproblem
topic: theory-of-computation
difficulty: advanced
featured: true
rating: 5
draft: false
---

> 本篇是[《论可计算数及其在判定问题中的应用》](/papers/zh/turing-computable-numbers/index.html)的**学习笔记版**，学习总结论文中的思想。

## 核心思想

图灵要回答的根本问题是：**什么叫“用有限手段计算”**。他把人的纸笔计算过程抽象为一台机器：有限个内部状态（m-构型）、一条划分为方格的无限纸带，以及只依赖当前状态与当前符号的有限规则。由此得到的图灵机模型，第一次让“算法”成为可以严格研究的对象。

论文完成三个关键动作：

1. **定义可计算**：无循环机器持续输出二进制序列，由此定义可计算实数。
2. **编码机器**：机器规则表可化为标准描述 S.D. 与描述数 D.N.，于是“程序”成为可以写在纸带上的数据。
3. **构造通用机器**：存在机器 $U$，读取任意机器的描述并模拟其行为，这是现代通用计算机、解释器和虚拟机的理论原型。

## 核心结论

1. **可计算数可枚举，但不能被有效枚举**：能为机器编号，却无法有效筛出哪些机器是无循环的。
2. **机器行为存在不可判定性**：不存在一般过程判定任意机器是否无循环，也不存在一般过程判定机器是否会打印某个给定符号。这是后来所谓“停机问题不可判定”的核心形态。
3. **对角论证不能滥用**：Cantor 式对角构造不能证明可计算序列不可枚举，因为构造出的对角序列未必可计算。
4. **判定问题不可解**：为每台机器 $M$ 构造公式 $Un(M)$，使得 $Un(M)$ 可证当且仅当 $M$ 曾经打印 0。若可判定公式可证性，就能判定机器是否打印 0，矛盾。因此希尔伯特判定问题没有机械解。
5. **机器模型与 $\lambda$-演算等价**：图灵可计算序列恰好是 $\lambda$-可定义序列，为“丘奇–图灵论题”奠定基础。

## 意义

- **工程意义**：程序即数据、通用机器模拟任意程序，是 CPU、解释器、虚拟机、编译器与操作系统运行机制的理论源头。
- **分析意义**：不存在完美的静态分析、缺陷检测和程序验证器；工具必须依赖约束、近似或人工输入。
- **理论意义**：可计算性、归约、不可判定性、图灵完备等概念由此展开，成为算法理论、程序语言与形式化方法的基础语言。
- **思想意义**：论文把“什么能被机械地完成”变成严格的数学问题，并给出边界；它既奠定计算理论，也划定了自动化能力的极限。

## 一句话总结

==程序可以被编码成数据，机器可以模拟任何机器，但并非所有关于程序的问题都能被自动回答。==
