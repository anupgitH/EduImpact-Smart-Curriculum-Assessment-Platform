![image_alt](https://github.com/anupgitH/EduImpact-Smart-Curriculum-Assessment-Platform/blob/68b2b88942f99c7f631e80099fef5a4358bd7bef/EduImpact.png)

# EduImpact — Smart Curriculum & Assessment Platform

Production-oriented full-stack starter: FastAPI, React + TypeScript + Vite, SQLAlchemy, MySQL, JWT authentication, Gemini question generation, courses, assessments, analytics.

## Run locally
Requirements: Python 3.11+, Node.js 20+. SQLite is used by default for a quick start; MySQL is supported through `DATABASE_URL`.

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
API: http://localhost:8000 · Swagger: http://localhost:8000/docs

### Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
Open http://localhost:5173. Register a teacher account to create courses and use AI question generation.

### MySQL
Create a database and least-privilege user, then set in `backend/.env`:
`DATABASE_URL=mysql+pymysql://eduimpact_user:YOUR_PASSWORD@localhost:3306/eduimpact`
For production set `AUTO_CREATE_TABLES=false` and use Alembic migrations.

## Included
- Registration/login with JWT and Argon2 password hashing
- Teacher/student roles and protected API endpoints
- Courses, assessments, attempts, objective grading
- Gemini-powered draft question generation
- Analytics summary endpoint
- Responsive React dashboard, course and assessment forms, AI question studio
- Backend smoke tests and CI workflow

## Before production
Read `SECURITY.md`. Configure strong secrets, HTTPS, exact CORS origins, database backups, migrations, rate limits, monitoring, account recovery, audit logging, and institution-level authorization. AI-generated content must be reviewed before use.
