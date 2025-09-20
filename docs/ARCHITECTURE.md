# Architecture

Money Trader is a modular platform consisting of:

- **Flutter Mobile App** – primary client delivering signals, alerts, and onboarding. Riverpod manages state and Dio handles HTTP interactions.
- **FastAPI Backend** – Python service providing REST, WebSocket, and background processing.
- **PostgreSQL & Redis** – persistent storage for users/portfolio and volatile cache for quotes/ratelimits.
- **Worker** – asyncio-based worker that monitors alerts and triggers notifications.
- **Dev Feeder** – synthetic price generator populating Redis in development.

## Data Flow
1. Feeder publishes prices to Redis (`price:{symbol}`) and OHLC structures.
2. API reads from Redis for market endpoints and broadcasts updates via `/ws/price`.
3. Mobile client subscribes to WebSocket for live tiles and uses REST for portfolio/alerts.
4. Alerts worker polls Redis + Postgres to mark triggered alerts and log notifications.

## Security & Compliance
- JWT auth with Argon2 password hashing.
- Audit log table tracks key actions (register/login/alert changes).
- Privacy endpoints allow export and deletion scheduling.
- Default headers and UI copy emphasise that no trades are executed and all content is educational.

## Extensibility
- Pricing providers abstracted for future integration with Binance, AlphaVantage, and Polygon.
- AI module exposes `predict`/`list_signals` stubs ready for ML replacements.
- Docker Compose orchestrates the full stack including observability (pgAdmin) and email (Mailhog).
