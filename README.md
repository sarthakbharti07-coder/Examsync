# ExamSync

**Prepare Smarter. Understand Patterns. Perform Better.**

ExamSync is an examination preparation platform designed to help students organize their syllabus, manage previous-year question papers, analyze examination patterns, and generate practice question papers.

## Features

### Implemented
- User signup and login.
- Protected application routes.
- Examination project management.
- PDF document upload.
- Syllabus creation and management.
- Unit, topic, and subtopic organization (currently in development).
- Dashboard with project information.

### Upcoming Features
- **Question Paper Management:** View, download, rename, and organize uploaded papers.
- **AI Syllabus Extraction:** Extract units and topics automatically from uploaded PDFs.
- **Pattern Analysis:** Identify repeated questions, important topics, and marks distribution.
- **AI Question Paper Generation:** Generate practice papers based on syllabus and previous-year patterns.
- **History:** Save generated papers and previous analysis.
- **Progress Tracking:** Track syllabus completion and preparation progress.
- **User Settings:** Profile management, preferences, and notifications.
- **Deployment:** Make ExamSync accessible online.

## Technology Stack

**Frontend**
- React
- TypeScript
- Vite
- React Router
- Axios
- Tailwind CSS

**Backend**
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

**Database**
- Supabase / PostgreSQL

## Project Structure

```text
ExamSync/
└── exampattern-backend/
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   │   └── v1/
    │   │   ├── models/
    │   │   ├── schemas/
    │   │   ├── db/
    │   │   └── main.py
    │   └── .env
    │
    ├── frontend/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   ├── services/
    │   │   ├── lib/
    │   │   └── App.tsx
    │   └── .env
    │
    └── README.md
```

## Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.12
- Node.js and npm
- Git
- A configured Supabase/PostgreSQL database

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd examsync/exampattern-backend
```

### 2. Backend Setup

Open a terminal in the project directory and run:

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory and configure the required environment variables.

Example:

```env
DATABASE_URL=your_database_connection_string
SECRET_KEY=your_secret_key
```

Use the exact variable names required by your backend configuration.

### 3. Frontend Setup

Open a second terminal:

```powershell
cd frontend
npm install
```

Configure the frontend API URL if required by your API client:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Running ExamSync Locally

You need **two separate terminals** to run the application.

### Terminal 1: Start the Backend

From the `exampattern-backend` directory:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Backend will run at:

`http://127.0.0.1:8000`

### Terminal 2: Start the Frontend

From the `exampattern-backend` directory:

```powershell
cd frontend
npm run dev
```

Frontend will run at:

`http://localhost:3000`

Open the frontend URL in your browser.

Keep both terminals running while using ExamSync.

## API Documentation

FastAPI provides interactive API documentation.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Development Roadmap

| Phase | Development |
|---|---|
| Phase 1 | Authentication, projects, document upload, and syllabus management |
| Phase 2 | Question paper management |
| Phase 3 | AI-powered syllabus extraction |
| Phase 4 | Examination pattern analysis |
| Phase 5 | AI question paper generation |
| Phase 6 | History and preparation tracking |
| Phase 7 | User settings and personalization |
| Phase 8 | Testing, optimization, and deployment |

## Security

- Never upload `.env` files to GitHub.
- Keep database passwords and API keys private.
- Validate uploaded files on the backend.
- Restrict access to each user's own projects and documents.
- Use secure environment variables in production.

---

**Project Status:** Actively under development.

**ExamSync — Your Smart Examination Preparation Companion.**
