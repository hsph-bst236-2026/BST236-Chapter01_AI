---
name: fetch-coingecko
description: Fetches top-10 cryptocurrency market data from the CoinGecko free API. Use this skill when you need to retrieve live crypto prices, market caps, volumes, and 24h price changes.
---

# Fetch CoinGecko Market Data

## Instructions

1. Use the CoinGecko **free** `/coins/markets` endpoint (no API key required):
   ```
   GET https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h
   ```

2. Use `curl` to make the request. Include a `User-Agent` header to avoid being blocked:
   ```bash
   curl -s -X GET "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h" \
     -H "Accept: application/json" \
     -H "User-Agent: CryptoWatchtower/1.0"
   ```

3. Save the raw JSON response to `data/market_data.json`.

4. **Retry logic**: If the request fails (non-200 status or empty response), wait 10 seconds and retry up to 3 times.

5. **Validation**: Ensure the response is valid JSON and contains an array with at least 1 entry. Each entry must have: `id`, `symbol`, `name`, `current_price`, `market_cap`, `total_volume`, `price_change_percentage_24h`.

## Expected Output Format

A JSON array saved to `data/market_data.json`:
```json
[
  {
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "current_price": 45000.00,
    "market_cap": 850000000000,
    "total_volume": 25000000000,
    "price_change_percentage_24h": -2.5,
    "image": "https://...",
    "last_updated": "2026-01-01T00:00:00.000Z"
  }
]
```

## Error Handling

- If the API is unreachable after 3 retries, create `data/market_data.json` with an empty array `[]` and print a warning message.
- Never crash the pipeline — always produce a valid (possibly empty) JSON file.
