# 24/7 Crypto Watchtower — Implementation Plan

## Problem Statement
Build a "24/7 Crypto Watchtower" that uses GitHub Copilot custom agents to orchestrate a data pipeline:
1. Fetch real-time cryptocurrency data from the CoinGecko API (top 10 coins by market cap)
2. Detect "Whale" movements (>5% price change in 24h)
3. Generate a visual HTML+Chart.js market report
4. Deploy a live dashboard to GitHub Pages

**Constraints**: Only create files in `.github/agents/`, `.github/skills/`, and `.github/prompts/`. No additional manual code — the agents generate all code at runtime.

---

## Architecture Overview

```
┌─────────────────┐
│  Orchestrator    │  (main agent — coordinates the pipeline)
│  Agent           │
└──────┬──────────┘
       │ invokes
       ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Data Fetcher │→ │ Whale        │→ │ Report       │→ │ Dashboard    │
│ Agent        │  │ Detector     │  │ Generator    │  │ Deployer     │
│              │  │ Agent        │  │ Agent        │  │ Agent        │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
     ↓ uses            ↓ uses            ↓ uses            ↓ uses
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ coingecko-   │  │ volatility-  │  │ chartjs-     │  │ gh-pages-    │
│ fetch skill  │  │ analysis     │  │ report skill │  │ deploy skill │
│              │  │ skill        │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## Workplan

### Phase 1: Skills (`.github/skills/`)
Skills define reusable capabilities that agents can invoke.

- [x] **1.1** Create `.github/skills/fetch-coingecko.md` — Skill to fetch top-10 crypto data from CoinGecko's free `/coins/markets` endpoint. Outputs JSON with price, market cap, 24h change, volume.
- [x] **1.2** Create `.github/skills/detect-whales.md` — Skill to analyze fetched data and flag coins with >5% absolute price change in 24h as "whale movements." Outputs a filtered list with severity labels.
- [x] **1.3** Create `.github/skills/generate-report.md` — Skill to produce a standalone HTML page with Chart.js visualizations: bar chart of 24h price changes, table of whale alerts, market summary cards.
- [x] **1.4** Create `.github/skills/deploy-gh-pages.md` — Skill to commit the generated HTML report to the `gh-pages` branch and push, triggering GitHub Pages deployment.

### Phase 2: Agents (`.github/agents/`)
Agents are autonomous actors that use skills to accomplish specific goals.

- [x] **2.1** Create `.github/agents/data-fetcher.md` — Agent responsible for fetching live crypto market data. Uses the `fetch-coingecko` skill. Handles rate-limiting, retries, and data validation.
- [x] **2.2** Create `.github/agents/whale-detector.md` — Agent that receives market data and identifies whale movements. Uses the `detect-whales` skill. Categorizes alerts by severity (moderate >5%, high >10%, extreme >20%).
- [x] **2.3** Create `.github/agents/report-generator.md` — Agent that takes market data + whale alerts and produces the HTML dashboard. Uses the `generate-report` skill. Ensures responsive design, dark theme, timestamp.
- [x] **2.4** Create `.github/agents/dashboard-deployer.md` — Agent that deploys the generated report to GitHub Pages. Uses the `deploy-gh-pages` skill. Handles branch creation if needed, commit messaging.
- [x] **2.5** Create `.github/agents/orchestrator.md` — Main coordinating agent that runs the full pipeline sequentially: fetch → detect → report → deploy. Handles errors, logs progress, and produces a summary.

### Phase 3: Prompts (`.github/prompts/`)
Prompts are reusable instructions the user invokes to trigger agent workflows.

- [x] **3.1** Create `.github/prompts/run-pipeline.prompt.md` — Master prompt that triggers the full watchtower pipeline end-to-end via the orchestrator agent.
- [x] **3.2** Create `.github/prompts/fetch-data.prompt.md` — Prompt to trigger only data fetching (useful for debugging).
- [x] **3.3** Create `.github/prompts/detect-whales.prompt.md` — Prompt to run whale detection on the latest data.
- [x] **3.4** Create `.github/prompts/generate-report.prompt.md` — Prompt to regenerate the dashboard report.
- [x] **3.5** Create `.github/prompts/deploy-dashboard.prompt.md` — Prompt to deploy the latest report to GitHub Pages.

### Phase 4: Directory Setup & Validation
- [x] **4.1** Create the `.github/agents/`, `.github/skills/`, and `.github/prompts/` directories.
- [x] **4.2** Verify all files are properly structured and cross-reference each other correctly.
- [x] **4.3** Validate the overall pipeline design is consistent and complete.

---

## File Manifest

| File | Purpose |
|------|---------|
| `.github/skills/fetch-coingecko.md` | CoinGecko API data fetching skill |
| `.github/skills/detect-whales.md` | Whale movement detection logic |
| `.github/skills/generate-report.md` | HTML+Chart.js report generation |
| `.github/skills/deploy-gh-pages.md` | GitHub Pages deployment |
| `.github/agents/data-fetcher.md` | Data fetching agent |
| `.github/agents/whale-detector.md` | Whale detection agent |
| `.github/agents/report-generator.md` | Report generation agent |
| `.github/agents/dashboard-deployer.md` | Dashboard deployment agent |
| `.github/agents/orchestrator.md` | Pipeline orchestration agent |
| `.github/prompts/run-pipeline.prompt.md` | Full pipeline execution prompt |
| `.github/prompts/fetch-data.prompt.md` | Data fetch only prompt |
| `.github/prompts/detect-whales.prompt.md` | Whale detection only prompt |
| `.github/prompts/generate-report.prompt.md` | Report generation only prompt |
| `.github/prompts/deploy-dashboard.prompt.md` | Dashboard deployment only prompt |

## Notes & Considerations

- **CoinGecko Free API**: Rate-limited to ~10-30 calls/min. The `fetch-coingecko` skill should use a single `/coins/markets` call to get all top-10 data in one request.
- **Whale Threshold Tiers**: Moderate (>5%), High (>10%), Extreme (>20%) — provides graduated severity for alerts.
- **Dashboard**: Self-contained single HTML file with inline Chart.js CDN link. No build step needed.
- **GitHub Pages**: Deploy to `gh-pages` branch. The deployer agent should handle the case where the branch doesn't exist yet.
- **Idempotency**: Each pipeline run should overwrite the previous report (single `index.html`), keeping the dashboard always current.
- **Error Handling**: The orchestrator should gracefully handle API failures (e.g., CoinGecko downtime) and still deploy a "data unavailable" dashboard rather than failing silently.
