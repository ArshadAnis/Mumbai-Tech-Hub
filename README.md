# Money Trader

Money Trader is a crypto and forex companion platform that delivers AI-assisted signals, configurable alerts, and portfolio insights without executing real trades. The stack includes a FastAPI backend, Flutter mobile app, Redis/PostgreSQL infrastructure, and developer tooling to launch quickly.

> **Disclaimer:** Money Trader does not provide financial advice or execute trades. Signals are educational only and trading involves risk.

## Repository Layout

```
backend/      FastAPI application, database models, workers, tests
mobile/       Flutter client for Android/iOS/web
feeder/       Synthetic data generator for development
ops/          Docker Compose environment and CI templates
web/landing/  Static marketing site with waitlist form
docs/         Product, security, and compliance documentation
scripts/      Helper scripts for local development and testing
```

## Quickstart

1. Copy `.env.example` to `.env` and customise secrets:
   ```bash
   cp .env.example .env
   ```
2. Launch the full stack (API, worker, Redis, Postgres, feeder, Mailhog):
   ```bash
   ./scripts/dev.sh
   ```
3. Visit the API docs at [http://localhost:8080/docs](http://localhost:8080/docs) when running in dev mode.
4. Run automated tests:
   ```bash
   ./scripts/test.sh
   ```
   Flutter tests are skipped automatically if the toolchain is unavailable.

## Backend Highlights

- JWT authentication with Argon2 password hashing and optional TOTP stubs.
- Market data endpoints backed by Redis with rate limiting.
- Portfolio management, AI signal stubs, billing tiers, and compliance utilities.
- WebSocket `/ws/price` endpoint for live price streaming.
- Async worker polls alerts and logs triggered notifications.
- Pytest suite covering health, market, and auth flows.

## Mobile App Highlights

- Flutter + Riverpod architecture with modular feature screens.
- Dio-based API client with interceptors for disclaimers and future auth.
- Live dashboards, signal cards, alert management, and news/calendar readers.
- In-app purchase and push messaging packages stubbed for production configuration.
- Widget test ensuring onboarding emphasises risk disclaimers.

## DevOps & CI

- `docker-compose` spins up API, worker, Postgres, Redis, Mailhog, pgAdmin, and feeder services.
- GitHub Actions workflows for backend (Poetry tests + Docker build) and Android (Flutter analyze/test/build) pipelines.
- Scripts ensure reproducible development setups and optional Flutter test gating.

## Compliance & Security

- Audit logging of critical user actions.
- GDPR/CCPA-ready export and deletion endpoints.
- Explicit disclaimers across API and UI surfaces.
- Documentation in `docs/` covering security posture, monetization plan, and compliance obligations.

## Troubleshooting

- Ensure Docker has sufficient resources (4 GB RAM+) for the Compose stack.
- If Redis/Postgres are not reachable, confirm ports `6379` and `5433` are free or update `docker-compose.yml` mappings.
- Flutter build issues: run `flutter doctor` and confirm SDK version `>=3.16.0`.

Happy building and stay compliant!
