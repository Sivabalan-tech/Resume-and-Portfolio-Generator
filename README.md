# AI Resume & Portfolio Builder 🤖

> Final Year MCA (Generative AI) Major Project — A production-ready, AI-powered resume and portfolio builder.

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org)
[![Gemini](https://img.shields.io/badge/Gemini-AI-orange)](https://ai.google.dev)

---

## 🚀 Features

| Feature | Description |
|---|---|
| **ATS Resume Generator** | Gemini AI generates ATS-optimized resumes with action verbs & keywords |
| **Cover Letter Writer** | Tailored, company-specific cover letters |
| **ATS Score Calculator** | SentenceTransformers + cosine similarity (0–100 score) |
| **Skill Gap Analysis** | Missing keyword detection from job descriptions |
| **Portfolio Generator** | About Me, LinkedIn summary, GitHub README, project descriptions |
| **PDF Export** | Download resume as beautifully styled PDF |
| **User Authentication** | JWT-based auth with bcrypt password hashing |
| **Role-Based Access** | User and Admin roles |
| **Admin Dashboard** | User management + platform analytics |
| **Resume History** | All generations saved and accessible |

---

## 🏗️ Tech Stack

**Frontend:** Next.js 14 (App Router) · TypeScript · Tailwind CSS · Axios

**Backend:** FastAPI · SQLAlchemy · SQLite · Uvicorn

**AI/ML:** Google Gemini API · SentenceTransformers (`all-MiniLM-L6-v2`) · NumPy

**Auth:** JWT (python-jose) · bcrypt (passlib)

**PDF:** xhtml2pdf (primary) · ReportLab (fallback)

---

## 📁 Project Structure

```
ai-resume-portfolio-builder/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Environment config
│   ├── database.py              # SQLAlchemy + SQLite
│   ├── models/                  # ORM models (User, Profile, ResumeHistory)
│   ├── schemas/                 # Pydantic schemas
│   ├── routers/                 # API endpoints
│   │   ├── auth.py              # POST /api/auth/register|login
│   │   ├── profile.py           # GET/PUT /api/profile
│   │   ├── resume.py            # POST /api/resume/generate
│   │   ├── cover_letter.py      # POST /api/cover-letter/generate
│   │   ├── ats.py               # POST /api/ats/analyze
│   │   ├── portfolio.py         # POST /api/portfolio/generate
│   │   ├── pdf.py               # POST /api/pdf/download
│   │   └── admin.py             # GET /api/admin/users|stats
│   ├── services/                # Business logic
│   │   ├── auth_service.py      # JWT + bcrypt
│   │   ├── ai_service.py        # Gemini API client
│   │   ├── ats_service.py       # SentenceTransformers scoring
│   │   └── pdf_service.py       # Markdown→PDF
│   ├── prompts/                 # Prompt templates
│   └── requirements.txt
└── frontend/
    └── src/
        ├── app/                 # Next.js App Router pages
        │   ├── page.tsx         # Landing page
        │   ├── login/           # Auth pages
        │   ├── register/
        │   ├── dashboard/       # User dashboard
        │   ├── profile/         # Profile builder
        │   ├── resume/          # Resume generator
        │   ├── cover-letter/    # Cover letter generator
        │   ├── ats/             # ATS analyzer
        │   ├── portfolio/       # Portfolio generator
        │   └── admin/           # Admin dashboard
        ├── components/
        │   └── DashboardLayout.tsx
        └── lib/
            ├── api.ts           # Axios client + typed helpers
            └── auth.tsx         # Auth context
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- A [Google Gemini API key](https://aistudio.google.com/)

---

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment

# Edit .env and add your GEMINI_API_KEY

# Start the server
uvicorn main:app --reload --port 8000
```

The backend API will be live at `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

---

### Frontend Setup

```bash
cd frontend

# Install dependencies (already done if you ran npm install)
npm install

# Configure environment
# .env.local already created with NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Frontend will be live at `http://localhost:3000`

---

## 🔑 Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | *required* |
| `SECRET_KEY` | JWT signing secret | change in production |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `60` |
| `DATABASE_URL` | Database URL | `sqlite:///./resume_builder.db` |
| `GEMINI_MODEL` | Gemini model name | `gemini-1.5-flash` |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API base URL |

---

## 📡 API Reference

### Authentication
```http
POST /api/auth/register    Body: {email, password, full_name, role}
POST /api/auth/login       Body: {email, password}
```

### Profile
```http
GET  /api/profile          Headers: Authorization: Bearer <token>
PUT  /api/profile          Body: {personal_info, skills, education, ...}
```

### Resume
```http
POST /api/resume/generate  Body: {job_role, job_description}
GET  /api/resume/history
GET  /api/resume/history/{id}
```

### ATS
```http
POST /api/ats/analyze      Body: {job_description, resume_text?}
```

### Cover Letter
```http
POST /api/cover-letter/generate  Body: {company_name, job_role, job_description}
```

### Portfolio
```http
POST /api/portfolio/generate
```

### PDF
```http
POST /api/pdf/download     Body: {markdown_text, filename}
GET  /api/pdf/history/{id}
```

### Admin (Admin Role Required)
```http
GET    /api/admin/users
GET    /api/admin/stats
DELETE /api/admin/users/{id}
```

---

## 🧪 API Testing — Sample cURL Commands

```bash
# 1. Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@mca.edu","password":"Test1234","full_name":"Test User","role":"user"}'

# 2. Login and get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@mca.edu","password":"Test1234"}'

# Store the token:  TOKEN=<access_token from above>

# 3. Update profile
curl -X PUT http://localhost:8000/api/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"personal_info":{"name":"Test User","email":"student@mca.edu"},"skills":["Python","React","Machine Learning"]}'

# 4. Generate resume
curl -X POST http://localhost:8000/api/resume/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"job_role":"Backend Developer","job_description":"Looking for Python FastAPI developer..."}'

# 5. ATS Analysis
curl -X POST http://localhost:8000/api/ats/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"job_description":"We need a Python developer with FastAPI, Docker, PostgreSQL experience."}'
```

---

## 🚀 Deployment

### Backend → Render.com (Free Tier)

1. Push code to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard

### Frontend → Vercel

1. Push frontend folder to GitHub
2. Import on [vercel.com](https://vercel.com)
3. Set `NEXT_PUBLIC_API_URL` to your Render backend URL
4. Deploy!

---

## 🔒 Security Notes

- Never commit `.env` to version control
- Change `SECRET_KEY` to a strong random string in production: `python -c "import secrets; print(secrets.token_hex(32))"`
- For production, switch `DATABASE_URL` to PostgreSQL

---

