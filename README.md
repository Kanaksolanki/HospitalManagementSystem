# AI-Powered Hospital Management System

Team: Riya (AI/ML) · Kanak (Frontend) · Diksha (Backend)

## Structure
- `backend/` — Django REST API (Diksha)
- `ai-module/` — AI/ML functions, models, notebooks (Riya)
- `frontend/` — React app (Kanak)

## Getting Started

### Backend
```
cd backend
python -m venv venv          # optional
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### AI Module
```
cd ai-module
pip install -r requirements.txt
```

### Frontend
```
cd frontend
npm install
npm run dev
```

See `API_CONTRACT.md` for the shared endpoint/data contract everyone builds against.
See `PROJECT_PLAN.md` for the full team workflow, timeline, and folder guide.
