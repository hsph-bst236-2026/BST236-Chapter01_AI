# Detect Whale Movements

Use the [whale-detector](../agents/whale-detector.md) agent to analyze the latest market data in `data/market_data.json` and identify whale movements.

Flag any coin with >5% absolute price change in 24h. Classify alerts as Moderate (>5%), High (>10%), or Extreme (>20%). Save results to `data/whale_alerts.json` and print a summary of findings.
