#!/usr/bin/env python3
"""Build static paper pages from papers/zh/*.md into docs/papers/zh/.

Requires: PyYAML, Markdown (pip install pyyaml markdown)
Run from anywhere: python3 tools/build_papers.py
"""

from __future__ import annotations

import html
import re
import shutil
import xml.etree.ElementTree as etree
from pathlib import Path

import markdown
import yaml
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "papers" / "zh"
ASSET_SOURCE_DIR = ROOT / "papers" / "assets"
OUTPUT_DIR = ROOT / "docs" / "papers" / "zh"
ASSET_OUTPUT_DIR = ROOT / "docs" / "papers"
HOME_PAGE = ROOT / "docs" / "index.html"
README_PAGE = ROOT / "README.md"
SOURCE_SITE = "https://peekdb.dev"
SITE_URL = "https://chirpyli.github.io/cs-paper-reading"
PREFIX = "../../../"
MARKERS = ("<!-- PAPERS START -->", "<!-- PAPERS END -->")
MARK_COLOR_PATTERN = "red|blue|green|orange|purple|gray"


class MarkInlineProcessor(InlineProcessor):
    """==text== / ==red:text== -> <mark> / <mark class="mark-red">."""

    def handleMatch(self, m, data):
        el = etree.Element("mark")
        color = m.group("color")
        if color:
            el.set("class", f"mark-{color}")
        el.text = m.group("text")
        return el, m.start(0), m.end(0)


class UnderlineInlineProcessor(InlineProcessor):
    """++text++ -> <u>text</u>."""

    def handleMatch(self, m, data):
        el = etree.Element("u")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class StrikeInlineProcessor(InlineProcessor):
    """~~text~~ -> <del>text</del>."""

    def handleMatch(self, m, data):
        el = etree.Element("del")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class MathPlaceholderPreprocessor(Preprocessor):
    """Hide TeX from Markdown inline rules before MathJax sees it."""

    def run(self, lines):
        text = "\n".join(lines)

        def store(match: re.Match[str]) -> str:
            token = f"MATHJAXTOKEN{len(self.md.math_tokens)}END"
            self.md.math_tokens.append((token, match.group(0)))
            return token

        text = re.sub(r"(?<!\\)\$\$.+?(?<!\\)\$\$", store, text, flags=re.S)
        text = re.sub(r"(?<!\\)\$(?!\$)([^$\n]+)(?<!\\)\$", store, text)
        return text.split("\n")


class MathPlaceholderPostprocessor(Postprocessor):
    """Restore TeX verbatim after Markdown conversion."""

    def run(self, text: str) -> str:
        for token, math in self.md.math_tokens:
            text = text.replace(token, math)
        return text


class PaperMarkdownExtension(Extension):
    """Obsidian-like inline annotations for paper notes."""

    def extendMarkdown(self, md):
        md.math_tokens = []
        md.preprocessors.register(MathPlaceholderPreprocessor(md), "math-placeholder-pre", 100)
        md.postprocessors.register(MathPlaceholderPostprocessor(md), "math-placeholder-post", 0)
        md.inlinePatterns.register(
            MarkInlineProcessor(
                r"==(?:(?P<color>" + MARK_COLOR_PATTERN + r"):)?(?P<text>[^=\n]+)==",
                md,
            ),
            "paper-mark",
            185,
        )
        md.inlinePatterns.register(
            UnderlineInlineProcessor(r"\+\+([^+\n]+)\+\+", md),
            "paper-underline",
            184,
        )
        md.inlinePatterns.register(
            StrikeInlineProcessor(r"~~([^~\n]+)~~", md),
            "paper-strike",
            183,
        )


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="%%DESCRIPTION%%">
  <title>%%TITLE%% · CS Paper Reading</title>
  <link rel="icon" type="image/svg+xml" href="%%PREFIX%%assets/favicon.svg">
  <link rel="stylesheet" href="%%PREFIX%%assets/style.css">
  <script>
    window.MathJax = {
      tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
      svg: { fontCache: 'global' }
    };
  </script>
  <script defer src="%%PREFIX%%assets/mathjax/tex-svg.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="%%PREFIX%%">cs-paper-reading</a>
      <nav aria-label="主导航">
        <a href="%%PREFIX%%#papers">论文笔记</a>
        <a href="%%PREFIX%%#repos">相关仓库</a>
        <a href="%%PREFIX%%#about">关于</a>
        <a class="header-github" href="https://github.com/chirpyli/cs-paper-reading" target="_blank" rel="noopener noreferrer" aria-label="cs-paper-reading on GitHub">
          <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
          </svg>
        </a>
      </nav>
    </div>
  </header>

  <main class="wrap paper-page">
    <article class="paper">
      <header class="paper-header">
        <p class="eyebrow">%%EYEBROW%%</p>
        <h1>%%TITLE%%</h1>
        <p class="paper-original">%%PAPER_TITLE%%</p>
        <p class="paper-authors">%%AUTHORS%%</p>
        <p class="paper-venue">%%VENUE%%</p>
        <div class="paper-tags">%%TAGS%%</div>
        <p class="paper-links">%%LINKS%%</p>
      </header>

      <details class="paper-toc">
        <summary>目录</summary>
        %%TOC%%
      </details>

      <div class="paper-body">
%%BODY%%
      </div>
    </article>

    <p class="paper-back"><a href="%%PREFIX%%#papers">← 返回论文笔记列表</a></p>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <span>© 2026 chirpyli</span>
      <span>Built with GitHub Pages</span>
    </div>
  </footer>
</body>
</html>
"""


def load_paper(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    _, raw_meta, body = text.split("---\n", 2)
    meta = yaml.safe_load(raw_meta) or {}
    return meta, body.strip()


def rewrite_links(body: str) -> str:
    """Rewrite links from the source site to paths valid in this project site."""
    def replace(match: re.Match[str]) -> str:
        prefix, url, suffix = match.groups()
        if url.startswith("../assets/"):
            return f"{prefix}../../{url[len('../assets/'):]}{suffix}"
        if url.startswith("/papers/zh/"):
            slug = url[len("/papers/zh/"):].removesuffix("/index.html").strip("/")
            return f"{prefix}../{slug}/{suffix}"
        if url.startswith("/zh/papers/"):
            slug = url[len("/zh/papers/"):].strip("/")
            return f"{prefix}../{slug}/{suffix}"
        if url.startswith("/zh/blog/"):
            return f"{prefix}{SOURCE_SITE}{url}{suffix}"
        if url.startswith("/papers/"):
            return f"{prefix}{PREFIX}{url.lstrip('/')}{suffix}"
        return match.group(0)

    return re.sub(r"(\]\()([^)\s]+)(\))", replace, body)


def copy_assets() -> None:
    """Copy markdown-side assets into the published site."""
    if not ASSET_SOURCE_DIR.exists():
        return
    for source in ASSET_SOURCE_DIR.rglob("*"):
        if not source.is_file():
            continue
        target = ASSET_OUTPUT_DIR / source.relative_to(ASSET_SOURCE_DIR)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def asset_url(url: str) -> str:
    if url.startswith("/"):
        return PREFIX + url.lstrip("/")
    return url


def render(meta: dict, body: str) -> tuple[str, str]:
    md = markdown.Markdown(
        extensions=["extra", "admonition", "toc", "sane_lists", PaperMarkdownExtension()],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )
    html_body = md.convert(rewrite_links(body))

    values = {
        "DESCRIPTION": html.escape(str(meta.get("description", ""))),
        "TITLE": html.escape(str(meta.get("title", ""))),
        "PREFIX": PREFIX,
        "PAPER_TITLE": html.escape(str(meta.get("paperTitle", ""))),
        "AUTHORS": html.escape(" · ".join(meta.get("authors", []))),
        "VENUE": html.escape(
            f"{meta.get('year', '')} · {meta.get('venue', '')}"
        ),
        "TAGS": "\n".join(
            f'          <span class="tag">{html.escape(str(tag))}</span>'
            for tag in meta.get("tags", [])
        ),
        "LINKS": (
            f'<a href="{html.escape(asset_url(meta["paperUrl"]))}">原文 PDF ↗</a>'
            if meta.get("paperUrl") else ""
        ),
        "EYEBROW": html.escape(
            " / ".join(str(x) for x in (meta.get("topic"), meta.get("difficulty")) if x)
        ),
        "TOC": md.toc,
        "BODY": html_body,
    }
    page = re.sub(
        r"%%([A-Z_]+)%%",
        lambda m: values.get(m.group(1), m.group(0)),
        PAGE_TEMPLATE,
    )
    return page, html_body


def update_home(papers: list[dict]) -> None:
    text = HOME_PAGE.read_text(encoding="utf-8")
    start, end = MARKERS
    if start not in text or end not in text:
        raise ValueError(f"{HOME_PAGE}: missing paper-list markers")

    items = []
    for paper in papers:
        items.append(
            "        <li>\n"
            f'          <a class="note-link" href="papers/zh/{paper["slug"]}/">{html.escape(paper["title"])}</a>\n'
            f'          <span class="note-desc">{html.escape(paper["description"])}</span>\n'
            f'          <span class="tag">{html.escape(str(paper["year"]))} · {html.escape(paper["venue"])}</span>\n'
            "        </li>"
        )
    block = (
        start
        + '\n      <ul class="note-list">\n'
        + "\n".join(items)
        + "\n      </ul>\n      "
        + end
    )
    updated = re.sub(
        re.escape(start) + r".*?" + re.escape(end),
        lambda _: block,
        text,
        flags=re.S,
    )
    HOME_PAGE.write_text(updated, encoding="utf-8")


def update_readme(papers: list[dict]) -> None:
    text = README_PAGE.read_text(encoding="utf-8")
    start, end = MARKERS
    if start not in text or end not in text:
        raise ValueError(f"{README_PAGE}: missing paper-list markers")

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|")

    def rating_stars(paper: dict) -> str:
        try:
            value = int(paper.get("rating", 5))
        except (TypeError, ValueError):
            value = 5
        value = max(1, min(5, value))
        return "★" * value + "☆" * (5 - value)

    lines = ["| 年份 | 论文 | 推荐程度 |", "| --- | --- | --- |"]
    for paper in papers:
        url = f"{SITE_URL}/papers/zh/{paper['slug']}/"
        lines.append(
            f"| {cell(paper.get('year', ''))} | "
            f"[{cell(paper['title'])}]({url}) | {rating_stars(paper)} |"
        )
    block = start + "\n" + "\n".join(lines) + "\n" + end
    updated = re.sub(
        re.escape(start) + r".*?" + re.escape(end),
        lambda _: block,
        text,
        flags=re.S,
    )
    README_PAGE.write_text(updated, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "docs" / ".nojekyll").touch()
    copy_assets()
    papers = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        meta, body = load_paper(path)
        if meta.get("draft"):
            continue
        slug = path.stem
        page, _ = render(meta, body)
        target = OUTPUT_DIR / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        papers.append({**meta, "slug": slug})

    papers.sort(key=lambda p: (int(p.get("year", 0)), p["slug"]))
    update_home(papers)
    update_readme(papers)
    print(f"Generated {len(papers)} paper pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
