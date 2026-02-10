# Run Full Watchtower Pipeline

Execute the complete 24/7 Crypto Watchtower pipeline end-to-end.

Use the [orchestrator](../agents/orchestrator.md) agent to run all four stages in sequence:

1. **Fetch** — Pull live market data for the top 10 cryptocurrencies from CoinGecko
2. **Detect** — Analyze the data for whale movements (>5% price change in 24h)
3. **Report** — Generate an HTML+Chart.js dashboard with visualizations and alerts
4. **Deploy** — Push the dashboard to GitHub Pages for live viewing

Run the full pipeline now and print the final summary when complete.
