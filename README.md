

# JobSync — AI-Powered Job Recommendation Platform

JobSync is a full-stack AI-powered ATS and Job Recommendation Platform that semantically matches resumes to real job listings fetched from live job APIs.

Upload your resume → Extract your skills → Get ranked job matches with missing skill analysis → Apply directly.

---

## Live Demo

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/docs`

---

## Features

- 📄 **Resume Upload** — Upload PDF resumes and extract text automatically
- 🧠 **AI Skill Extraction** — Detects technical skills from resume content
- 🔍 **Semantic Matching** — Uses Sentence Transformers + cosine similarity to match resumes to jobs beyond keyword matching
- 💼 **Real Job Listings** — Fetches live jobs from Adzuna API with Apply Now links
- 📊 **Match Scoring** — Ranks jobs by compatibility percentage
- ❌ **Missing Skill Analysis** — Shows exactly which skills you need for each role
- 🔐 **Authentication** — JWT-based login/signup with protected routes
- 📁 **Resume History** — Dashboard showing all past uploads and detected skills

---

## Tech Stack

### Backend
- Python, FastAPI, Uvicorn
- PostgreSQL, SQLAlchemy
- Sentence Transformers (`all-MiniLM-L6-v2`)
- JWT Auth (`python-jose`, `passlib`)
- Adzuna Jobs API
- PyPDF2

### Frontend
- React, Vite
- React Router DOM
- Axios
- CSS Modules

## Author

**Samidha Mane**  
[GitHub](https://github.com/samidha-mane)
