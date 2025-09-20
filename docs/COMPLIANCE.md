# Compliance Strategy

Money Trader is a non-custodial analytics platform. The following controls are implemented:

- **Disclaimers**: All channels (API, mobile, docs) reiterate that content is educational and not investment advice.
- **KYC/PII**: Minimal data stored – email and optional name. Audit logs avoid sensitive data.
- **GDPR/CCPA**: `/privacy/export` and `/privacy/delete` endpoints facilitate subject rights. Data deletion is soft-flagged for manual review.
- **Security**: Argon2 password hashing, JWT access/refresh tokens, optional TOTP stub, HTTPS enforcement recommended in production.
- **Logging**: Centralised, PII-safe logs with user ID references only.
- **Affiliate Transparency**: Referral modules must label partner content clearly in UI and API responses.
- **Risk Disclosure**: App surfaces warnings during onboarding, settings, and signal views.
