# Money Trader API

## Overview
The Money Trader API provides secure endpoints for crypto and forex signals, alerts, and portfolio analytics. All responses include disclaimers reminding users that no financial advice is provided.

## Authentication
- JWT bearer tokens issued via `/auth/login` and `/auth/refresh`.
- Optional TOTP verification endpoints are stubbed for future integration.

## Public Endpoints
- `GET /health` – service check.
- `GET /market/symbols` – available instruments filtered by market.
- `GET /market/price` – latest cached quote.
- `GET /market/ohlc` – OHLC candles from Redis cache.
- `GET /news` / `GET /calendar` – mocked sources with caching.
- `GET /ws/price` – WebSocket stream providing JSON ticks.

## Authenticated Endpoints
- `/me` – current user profile and tier limits.
- `/portfolio` – list positions, add manual entries, retrieve analytics.
- `/alerts` – CRUD for price alerts, test trigger helper.
- `/signals` – AI stub delivering per-symbol strategies with confidence.
- `/billing` – subscription tiers and webhook stub.
- `/privacy` – GDPR/CCPA tooling for export and deletion requests.
- `/admin/stats` – admin-only metrics.

## Rate Limiting
A Redis-backed token bucket limits repeated access to market endpoints. Defaults can be tuned with `RATE_LIMIT_*` environment variables.

## Errors
Errors follow FastAPI’s standard JSON structure with descriptive messages. Sensitive details are avoided to maintain compliance.
