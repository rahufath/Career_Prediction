# AI Career Guidance System

A premium AI-driven career interview and guidance platform that uses real-time emotion analysis and personality prediction.

## 📁 Project Structure

```text
├── backend/            # Professional FastAPI server
│   ├── app/            # Modular application logic (Services, Schemas, Utils)
│   ├── models/         # Trained AI model files (.pkl)
│   ├── data/           # Training datasets
│   ├── scripts/        # Utility scripts (training, diagnosis)
│   ├── main.py         # Concise entry point
│   └── requirements.txt
├── frontend/           # Next.js web application
│   ├── src/
│   │   ├── hooks/      # Custom React hooks (useInterview)
│   │   ├── types/      # Centralized TypeScript definitions
│   │   ├── components/features/ # Feature-based modular components
│   │   └── components/ui/       # Base UI primitives
│   └── package.json
└── docs/               # Project summaries and logs
```

## 🚀 Quick Start Instructions

### 1. Backend Setup (Python)
Navigate to the backend directory and install dependencies:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
*Server runs on: [http://localhost:8000](http://localhost:8000)*

### 2. Frontend Setup (Next.js)
In a new terminal, navigate to the frontend directory:
```powershell
cd frontend
npm install
npm run dev
```
*Application runs on: [http://localhost:3000](http://localhost:3000)*

## 🧹 Maintenance
Run the included `cleanup_project.ps1` at any time to remove cache files, logs, and temporary items.

```powershell
.\cleanup_project.ps1
```
