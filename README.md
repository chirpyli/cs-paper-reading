# cs-paper-reading

计算机科学论文阅读笔记与相关代码仓库索引，通过 GitHub Pages 发布为项目站点。

## 站点地址

本仓库对应：

```
https://chirpyli.github.io/cs-paper-reading/
```

## 论文列表

列表由构建脚本根据 `papers/zh/*.md` 自动生成。

<!-- PAPERS START -->
| 年份 | 论文 | 推荐原因 |
| --- | --- | --- |
| 1936 | [论可计算数及其在判定问题中的应用](https://chirpyli.github.io/cs-paper-reading/papers/zh/turing-computable-numbers/) | 图灵 1936 年奠基性论文全文：自动机、可计算序列、通用机、对角论证、判定问题不可解性，并附论文修正与注释 |
| 1946 | [电子计算仪器逻辑设计的初步讨论](https://chirpyli.github.io/cs-paper-reading/papers/zh/ias-computer-logical-design/) | IAS 1946 年报告全文：并行存储程序计算机、Selectron 存储器、40 位字长、累加器、乘除法、指令编码与控制器的逻辑设计 |
| 1948 | [通信的数学理论](https://chirpyli.github.io/cs-paper-reading/papers/zh/shannon-mathematical-theory-of-communication/) | 香农 1948 年信息论奠基论文全文中文翻译：信息熵、信道容量、编码定理、有噪信道、连续信道、率失真理论与数学附录 |
| 1955 | [关于举办达特茅斯人工智能夏季研究项目的提案](https://chirpyli.github.io/cs-paper-reading/papers/zh/dartmouth-ai-proposal/) | 1955 年达特茅斯人工智能提案全文中文翻译：人工智能研究纲领、自动计算机、语言、神经网络、计算复杂性、自我改进、抽象、随机性与创造性，以及四位发起人的研究计划 |
| 1965 | [把更多元件塞进集成电路](https://chirpyli.github.io/cs-paper-reading/papers/zh/moore-cramming-more-components/) | 摩尔 1965 年原文中文翻译：集成电路元件数、成本曲线、每年翻倍趋势、良率、散热、线性电路与摩尔定律的提出 |
| 1970 | [大型共享数据库的关系模型](https://chirpyli.github.io/cs-paper-reading/papers/zh/codd-relational-model/) | Codd 1970 年经典论文全文中文翻译：提出关系模型、规范化形式、数据子语言，并讨论关系运算、冗余与一致性 |
| 1970 | [虚拟内存](https://chirpyli.github.io/cs-paper-reading/papers/zh/denning-virtual-memory/) | Denning 1970 年经典综述《Virtual Memory》全文，逐节还原虚拟存储器的动机、机制、策略、局部性原理与工作集理论 |
| 1974 | [SEQUEL：一种结构化的英语查询语言](https://chirpyli.github.io/cs-paper-reading/papers/zh/sequel/) | SEQUEL 原始论文全文中文翻译：以 SELECT-FROM-WHERE 块、映射、GROUP BY 与集合运算取代谓词演算中的量词和绑定变量，是 SQL 的直接前身 |
| 1974 | [UNIX 分时系统的设计与实现](https://chirpyli.github.io/cs-paper-reading/papers/zh/unix-time-sharing-system/) | Ritchie 与 Thompson 1974 年 UNIX 论文全文中文翻译：文件系统、i-node、Shell、进程、管道、fork/exec、重定向、过滤器、陷阱、系统统计与设计哲学 |
| 1976 | [System R：面向数据库管理的关系方法](https://chirpyli.github.io/cs-paper-reading/papers/zh/system-r/) | System R 原始论文全文中文翻译：RDS/RSS 两层架构、SEQUEL 接口、基于代价的优化器、事务与并发控制、检查点恢复，以及 RDI/RSI 操作符与语法附录 |
| 1978 | [分布式系统中的时间、时钟与事件排序](https://chirpyli.github.io/cs-paper-reading/papers/zh/lamport-clocks/) | Lamport 奠基性论文：用“先于发生”关系定义分布式系统中的偏序，用逻辑时钟扩展为全序，并给出物理时钟同步算法与偏差上界 |
| 2014 | [Raft：寻找一种易于理解的共识算法](https://chirpyli.github.io/cs-paper-reading/papers/zh/raft/) | Raft 通过强领导者、随机选举超时与联合共识，把 Paxos 难以理解的共识问题分解为可独立理解的Leader选举、日志复制与安全性 |
| 2016 | [Snowflake 弹性数据仓库](https://chirpyli.github.io/cs-paper-reading/papers/zh/snowflake/) | Snowflake 提出多集群共享数据架构，为云端数据仓库提供弹性、半结构化数据支持、时间旅行与端到端安全 |
| 2017 | [Amazon Aurora: 面向高吞吐云原生关系数据库的设计考量](https://chirpyli.github.io/cs-paper-reading/papers/zh/aurora/) | Aurora 将 redo 日志处理下推到多租户横向扩展存储服务，把云数据库的核心瓶颈从计算与存储转移到网络 |
| 2019 | [Socrates: 云端新 SQL Server](https://chirpyli.github.io/cs-paper-reading/papers/zh/socrates/) | Socrates 将 SQL Server 分解为计算、日志、页面与对象存储层，实现云数据库的弹性扩展与高可用 |
| 2026 | [DeepSeek Elastic Compute (DSec)：面向大规模高效智能体训练的沙箱基础设施](https://chirpyli.github.io/cs-paper-reading/papers/zh/deepseek-elastic-compute/) | DSec 通过四类沙箱后端、集群级放置与生命周期管理、版本化层组合和 3FS 按需镜像加载，支撑大规模智能体训练 |
| 2026 | [Lakebase：把 OLTP 重建为开放湖存储之上的弹性计算](https://chirpyli.github.io/cs-paper-reading/papers/zh/lakebase/) | Databricks 提出 Lakebase：第三代事务数据库架构，把全部存储外置到云对象存储并采用开放 PostgreSQL 页格式，实现存算分离、零拷贝分支与 Lakehouse 统一分析 |
| 2026 | [时空可组合性的编程范式](https://chirpyli.github.io/cs-paper-reading/papers/zh/spatiotemporal-composability/) | 提出可逆效应与响应式协效应，将效应与协效应上下文统一为上下文范式，在 Cordis 中实现运行时组件的时空可组合性 |
<!-- PAPERS END -->

## 目录结构

```
.
├── papers/                   # 论文 Markdown 源文件（唯一需要日常维护的目录）
│   └── zh/*.md               # 每篇论文一个文件，含 frontmatter
├── docs/                     # 构建产物 + 站点静态资源
│   ├── index.html            # 首页，论文列表由构建脚本自动同步
│   ├── assets/style.css      # 全站样式（含高亮/下划线样式）
│   ├── assets/favicon.svg    # 站点图标
│   ├── papers/
│   │   ├── zh/<slug>/index.html  # 生成的论文页面
│   │   ├── lakebase/             # 论文配图
│   │   └── *.pdf                 # 原论文 PDF
│   └── .nojekyll             # 禁用 Jekyll，原样发布静态文件
├── tools/build_papers.py     # Markdown → 静态页面生成脚本
├── .github/workflows/
│   └── deploy-pages.yml      # 推送后自动构建并发布到 GitHub Pages
├── requirements.txt          # 构建依赖
├── LICENSE
└── README.md
```

## 启用 GitHub Pages（一次性操作）

1. 先把本站文件提交并推送到远端：

   ```bash
   git add .
   git commit -m "Set up GitHub Pages with Actions"
   git push origin master
   ```

2. 打开仓库的 GitHub 网页：`https://github.com/chirpyli/cs-paper-reading`

3. 进入 **Settings → Pages**。

4. 在 **Build and deployment** 中：

   - **Source** 选择 `GitHub Actions`
   - 点击 **Save**

5. 推送后 `.github/workflows/deploy-pages.yml` 会自动构建 `docs/` 并发布。
   等待几十秒到几分钟，刷新 `https://chirpyli.github.io/cs-paper-reading/` 即可看到页面。

> 构建脚本仍会把结果写入 `docs/`，因此也可以继续用 `Deploy from a branch → master / docs`。
> 但推荐切换为 `GitHub Actions`，这样本地只需要维护 `papers/` 下的 Markdown。

## 日常发布：只需新增一篇 Markdown

1. 在 `papers/zh/` 下新增文件。文件命名规则：
   - 论文全文翻译：`YYYY-paper-slug.md`，例如 `2026-lakebase.md`；
   - 个人学习笔记：`YYYY-paper-slug-notes.md`，例如 `2026-lakebase-notes.md`。
   - `slug` 使用小写英文与连字符，不使用空格、中文或下划线；文件名年份应与 `year` 一致。
2. 复制已有笔记的 frontmatter，按需修改：

   ```yaml
   ---
   title: "中文标题"
   paperTitle: "Paper Title"
   slug: my-paper
   authors: ["Author A", "Author B"]
   year: 2026
   venue: "Conference / Journal"
   paperUrl: "/papers/my-paper.pdf"
   paperUrlZh: "/papers/zh/my-paper/index.html"
   description: "一句话摘要，会显示在首页和 README 推荐原因列"
   reason: "推荐原因（可选，未填写时使用 description）"
   lang: zh
   tags: [database, systems]
   topic: systems
   difficulty: intermediate
   featured: false
   draft: false   # true 时不会生成页面，适合写作中
   ---
   ```

`slug` 决定页面 URL，因此文件以后需要改名时，只要保持 `slug` 不变，链接就不会失效。
README 论文列表的“推荐原因”列优先取 frontmatter 的 `reason`，未填写时使用 `description`。`slug` 以 `-notes` 结尾的学习笔记不会出现在该列表中，但仍会在站点首页展示。

3. 提交并推送：

   ```bash
   git add papers/zh/my-paper.md
   git commit -m "Add note: my paper"
   git push origin master
   ```

4. GitHub Actions 自动运行 `tools/build_papers.py`，生成
   `docs/papers/zh/my-paper/index.html`、刷新首页列表，并发布到 Pages。

本地预览（可选）：

```bash
pip install -r requirements.txt
python3 tools/build_papers.py
python3 -m http.server 8000 --directory docs
```

## 论文笔记中的 Markdown 写法

| 想实现的效果 | 在 Markdown 中写 | 生成结果 |
| --- | --- | --- |
| 加粗 | `**重点**` | **重点** |
| 斜体 | `*强调*` | *强调* |
| 黄色高亮 | `==重点==` | <mark>重点</mark> |
| 彩色高亮 | `==red:结论==` | <mark class="mark-red">结论</mark> |
| 下划线 | `++关键字++` | <u>关键字</u> |
| 删除线 | `~~旧结论~~` | <del>旧结论</del> |
| 告示块 | `!!! note "标题"` + 缩进内容 | 带左边框的提示卡片 |

彩色高亮支持：`red`、`blue`、`green`、`orange`、`purple`、`gray`。
例如：

```markdown
==这是黄色高亮==，==red:这是红色高亮==，++这是下划线++，**==重要结论==**。
```

也可以使用原生 HTML：`<mark class="mark-blue">蓝色</mark>`、`<u>下划线</u>`。

## 图片与 PDF

图片放在 `papers/assets/` 下，按论文分目录，与 Markdown 源文件一起维护：

```text
papers/
├── assets/
│   └── lakebase/
│       └── fig-1.png
├── zh/
│   └── 2026-lakebase.md
└── en/
    └── lakebase-2026.md
```

在 Markdown 中使用相对于当前文件的路径引用：

```markdown
![架构图](../assets/lakebase/fig-1.png)
```

这样 VS Code 等编辑器的 Markdown 预览可以直接显示图片。构建脚本会把
`papers/assets/` 下的文件复制到 `docs/papers/`，并自动改写为网站可访问的路径，
不需要维护两份图片。

PDF 仍可放在 `docs/papers/` 下，用根路径引用：

```markdown
原文：[Paper](/papers/lakebase-2026.pdf)
```

frontmatter 中写：

```yaml
paperUrl: "/papers/lakebase-2026.pdf"
```

构建脚本会自动把 `/papers/...` 改写为适合 GitHub Pages 子路径的相对链接。

## 自定义域名（可选）

在仓库根目录添加 `CNAME` 文件（内容为你的域名，如 `notes.example.com`），并在域名服务商处配置 CNAME 指向 `chirpyli.github.io`。然后在 **Settings → Pages → Custom domain** 中填写该域名。
