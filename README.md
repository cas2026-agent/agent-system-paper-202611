# Agent 系统论文精读

网页：https://cas2026-agent.github.io/agent-system-paper-202611/

按系统层次精读 Agent 系统论文，共 29 篇。总览页给出层次图，标出每篇论文所在的位置。

单独页面（17 篇）：

| 分组 | 论文 |
|---|---|
| 评测与负载 | AgentBoard、The Cost of Dynamic Reasoning、AgentSysBench、From Requests to Sessions、XPerf |
| 编排与推理服务 | AgentServeSim、Murakkab、Agentix、ConServe（Observation, Not Prediction）、CacheScout |
| 模拟器 | LLMServingSim 2.0、Simthesizer |
| 沙箱与状态 | DeltaBox、Crab、SpecBox、YoloFS、Safe to Resume |

速览页（12 篇，每篇讲问题、做法和主要结果）：τ-bench、SWE-Bench Pro、MLR-Bench、TRACE、AgentSuite、Tree-GRPO、AIOS、SGLang、Mooncake、JITServe、ServeGen、Vidur。

## 目录

- `src/shell.html`：页面外壳（样式、标签页、脚本）
- `src/papers/<id>.html`：每篇论文的讲解，`briefs.html` 是速览页，`overview.html` 是总览页
- `figures/<id>/`：论文原图
- `papers/`：论文 PDF，用 Git LFS 跟踪（克隆前先装 `git lfs`）
- `build.py`：把外壳和各篇讲解拼成 `index.html`，同时检查引文编号

## 构建与发布

```sh
python3 build.py
```

推送到 `main` 后，`.github/workflows/pages.yml` 会运行 `build.py`，给 `index.html` 补上 doctype、charset 和 viewport，再连同 `figures/` 一起部署到 GitHub Pages。
