# Agent 系统论文精读

网页：https://cas2026-agent.github.io/agent-system-paper-202611/

按系统层次精读六篇 Agent 系统论文：AgentBoard、DeltaBox、LLMServingSim 2.0、AgentServeSim、The Cost of Dynamic Reasoning、Crab。

## 目录

- `src/shell.html`：页面外壳（样式、标签页、脚本）
- `src/papers/<id>.html`：每篇论文的讲解
- `figures/<id>/`：论文原图
- `papers/`：论文 PDF，用 Git LFS 跟踪（克隆前先装 `git lfs`）
- `build.py`：把外壳和各篇讲解拼成 `index.html`，同时检查引文编号

## 构建与发布

```sh
python3 build.py
```

推送到 `main` 后，`.github/workflows/pages.yml` 会运行 `build.py`，给 `index.html` 补上 doctype、charset 和 viewport，再连同 `figures/` 一起部署到 GitHub Pages。
