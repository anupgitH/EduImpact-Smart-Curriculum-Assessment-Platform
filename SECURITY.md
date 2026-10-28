# Security checklist
This is a production-oriented starter, not a security certification.
- Replace `SECRET_KEY` with a unique, strong random secret and store it in a secret manager.
- Use HTTPS, exact CORS origins, a least-privilege MySQL account, backups and restore tests.
- Set `ENVIRONMENT=production`, `DEBUG=false`, `AUTO_CREATE_TABLES=false`; run Alembic migrations.
- Add gateway rate limiting, email verification, password recovery, account abuse controls, monitoring and audit logs.
- Review authorization and resource ownership before public deployment; add institution-level tenancy checks if multiple institutions will share the system.
- Do not expose AI provider keys in frontend variables. Do not send student personal data to an AI provider without policy approval.
- Require educator review of AI-generated questions and answer keys.
