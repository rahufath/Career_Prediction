# AI Career Guidance System

A premium AI-driven career interview and guidance platform that uses real-time emotion analysis and personality prediction.

## 📁 Project Structure

```text
├── backend/            # Professional FastAPI server
│   ├── app.py          # Main FastAPI entry point
│   ├── models/         # Trained AI model files (.joblib, .pth, .pkl)
│   ├── data/           # Training datasets (dataset.csv)
│   ├── service/        # Core business logic and API models
│   ├── lib/            # Utility functions and helper modules
│   ├── Module_Training/# Jupyter notebooks for model development
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
python app.py
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

