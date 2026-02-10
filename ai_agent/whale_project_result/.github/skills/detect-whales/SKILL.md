---
name: detect-whales
description: Analyzes cryptocurrency market data to identify whale movements — coins with >5% absolute price change in 24h. Use this skill when you need to flag high-volatility coins and classify them by severity.
---

# Detect Whale Movements

## Instructions

1. Read the market data from `data/market_data.json`.

2. For each coin, examine the `price_change_percentage_24h` field.

3. Flag coins based on **absolute value** of 24h price change using these severity tiers:
   - 🟡 **Moderate**: |change| > 5% and ≤ 10%
   - 🟠 **High**: |change| > 10% and ≤ 20%
   - 🔴 **Extreme**: |change| > 20%

4. For each flagged coin, record:
   - `id`, `symbol`, `name`
   - `price_change_percentage_24h` (original signed value)
   - `severity` (one of: `moderate`, `high`, `extreme`)
   - `direction` (one of: `pump` if positive, `dump` if negative)

5. Sort whale alerts by absolute price change (descending — most volatile first).

6. Write the results to `data/whale_alerts.json`.

## Expected Output Format

A JSON array saved to `data/whale_alerts.json`:
```json
[
  {
    "id": "dogecoin",
    "symbol": "doge",
    "name": "Dogecoin",
    "current_price": 0.15,
    "price_change_percentage_24h": -12.3,
    "severity": "high",
    "direction": "dump"
  }
]
```

If no coins exceed the 5% threshold, output an empty array `[]`.

## Error Handling

- If `data/market_data.json` is missing or empty, output an empty array `[]` to `data/whale_alerts.json`.
- If a coin is missing the `price_change_percentage_24h` field, skip it.
