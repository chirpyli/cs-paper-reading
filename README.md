# cs-paper-reading

计算机科学论文阅读笔记与相关代码仓库索引，通过 GitHub Pages 发布为项目站点。

## 站点地址

项目站点的固定格式为：

```
https://<用户名>.github.io/<仓库名>/
```

本仓库对应：

```
https://chirpyli.github.io/cs-paper-reading/
```

## 目录结构

```
.
├── docs/               # 站点源文件（GitHub Pages 的发布目录）
│   ├── index.html      # 首页
│   ├── assets/
│   │   └── style.css   # 样式
│   └── .nojekyll       # 禁用 Jekyll，原样发布静态文件
├── LICENSE
└── README.md
```

## 启用 GitHub Pages（一次性操作）

1. 先把本站文件提交并推送到远端：

   ```bash
   git add .
   git commit -m "Add GitHub Pages project site"
   git push origin master
   ```

2. 打开仓库的 GitHub 网页：`https://github.com/chirpyli/cs-paper-reading`

3. 进入 **Settings → Pages**（左侧栏）。

4. 在 **Build and deployment** 中：

   - **Source** 选择 `Deploy from a branch`
   - **Branch** 选择 `master`
   - **Folder** 选择 `/docs`
   - 点击 **Save**

5. 等待几十秒到几分钟，刷新 `https://chirpyli.github.io/cs-paper-reading/` 即可看到页面。

## 日常更新

修改 `docs/` 下的文件后，正常提交推送即可，GitHub Pages 会自动重新发布：

```bash
git add docs/
git commit -m "Update site"
git push origin master
```

## 可选：改用 GitHub Actions 发布

如果以后需要构建步骤（例如 Jekyll / Hugo / Vite），可以改为 Actions 发布：

1. 在 **Settings → Pages → Source** 选择 `GitHub Actions`。
2. 新增 `.github/workflows/deploy-pages.yml`，在构建步骤后上传 `docs/` 作为 artifact，再用 `actions/deploy-pages@v4` 部署。

这样可以把站点源文件和构建产物彻底分离。

## 自定义域名（可选）

在仓库根目录添加 `CNAME` 文件（内容为你的域名，如 `notes.example.com`），并在域名服务商处配置 CNAME 指向 `chirpyli.github.io`。然后在 **Settings → Pages → Custom domain** 中填写该域名。
