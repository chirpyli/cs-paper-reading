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
| 年份 | 论文 | 推荐程度 |
| --- | --- | --- |
| 1970 | [关系模型的诞生](https://chirpyli.github.io/cs-paper-reading/papers/zh/codd-relational-model/) | ★★★★★ |
| 1974 | [SQL 的前身：SEQUEL 的诞生](https://chirpyli.github.io/cs-paper-reading/papers/zh/sequel-1974/) | ★★★★★ |
| 1976 | [System R：关系数据库管理的里程碑](https://chirpyli.github.io/cs-paper-reading/papers/zh/system-r-1976/) | ★★★★★ |
| 1978 | [分布式系统中的时间、时钟与事件排序](https://chirpyli.github.io/cs-paper-reading/papers/zh/lamport-clocks-1978/) | ★★★★★ |
| 1978 | [分布式系统中的时间、时钟与事件序列（学习笔记）](https://chirpyli.github.io/cs-paper-reading/papers/zh/lamport-clocks-study-notes/) | ★★★★☆ |
| 2014 | [Raft：寻找一种易于理解的共识算法](https://chirpyli.github.io/cs-paper-reading/papers/zh/raft-2014/) | ★★★★★ |
| 2014 | [Raft 共识算法（学习笔记）](https://chirpyli.github.io/cs-paper-reading/papers/zh/raft-study-notes/) | ★★★★☆ |
| 2016 | [Snowflake 弹性数据仓库](https://chirpyli.github.io/cs-paper-reading/papers/zh/snowflake-2016/) | ★★★★★ |
| 2017 | [Amazon Aurora: 面向高吞吐云原生关系数据库的设计考量](https://chirpyli.github.io/cs-paper-reading/papers/zh/aurora-2017/) | ★★★★★ |
| 2017 | [Aurora 核心机制阅读札记](https://chirpyli.github.io/cs-paper-reading/papers/zh/aurora-analysis/) | ★★★☆☆ |
| 2019 | [Socrates: 云端新 SQL Server](https://chirpyli.github.io/cs-paper-reading/papers/zh/socrates-2019/) | ★★★★☆ |
| 2026 | [DeepSeek Elastic Compute (DSec)：面向大规模高效智能体训练的沙箱基础设施](https://chirpyli.github.io/cs-paper-reading/papers/zh/deepseek-elastic-compute-2026/) | ★★★★☆ |
| 2026 | [Lakebase：把 OLTP 重建为开放湖存储之上的弹性计算](https://chirpyli.github.io/cs-paper-reading/papers/zh/lakebase-2026/) | ★★★★★ |
| 2026 | [时空可组合性的编程范式](https://chirpyli.github.io/cs-paper-reading/papers/zh/spatiotemporal-composability-2026/) | ★★★★☆ |
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

1. 在 `papers/zh/` 下新增文件，例如 `my-paper.md`。文件名即页面 URL 中的 `<slug>`。
2. 复制已有笔记的 frontmatter，按需修改：

   ```yaml
   ---
   title: "中文标题"
   paperTitle: "Paper Title"
   authors: ["Author A", "Author B"]
   year: 2026
   venue: "Conference / Journal"
   paperUrl: "/papers/my-paper.pdf"
   description: "一句话摘要，会显示在首页"
   lang: zh
   tags: [database, systems]
   topic: systems
   difficulty: intermediate
   featured: false
   rating: 4      # 1-5 星，控制 README 论文列表中的推荐程度
   draft: false   # true 时不会生成页面，适合写作中
   ---
   ```

`rating` 取值 1–5，会显示为 README 论文列表中的推荐星级。

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
│   └── lakebase-2026.md
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
