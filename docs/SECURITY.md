# Security Controls

- **Authentication**: JWT access/refresh pair with rotation, bearer tokens required for protected endpoints.
- **Password Hashing**: Argon2 via `passlib` with configurable parameters.
- **Transport**: TLS termination expected at ingress. CSP, CORS restricted via configuration.
- **Secrets Management**: `.env` values injected at runtime; repository ships with `.env.example` only.
- **Audit Trails**: `audit_logs` table captures IP, action, and metadata for key events.
- **Rate Limiting**: Redis token bucket protects high-traffic endpoints.
- **Dependency Updates**: Poetry + GitHub Actions keep dependencies current.
- **Static Analysis & Tests**: CI executes lint/tests for backend and Flutter to catch regressions.
