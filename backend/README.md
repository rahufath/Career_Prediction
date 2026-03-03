# AI Career Prediction Backend

FastAPI-based intelligence engine for facial emotion analysis and career recommendation.

## 📁 System Architecture

- **`app.py`**: Main application entry point that manages REST and WebSocket endpoints.
- **`service/`**: Core intelligence services.
  - `career_guide_service.py`: Orchestrates the Emotion -> Personality -> Career prediction pipeline.
  - `api_models.py`: Pydantic data schemas for request/response validation.
  - `constants.py`: Interview questions and detailed career path Metadata.
- **`lib/`**: Helper modules for data aggregation, insight generation, and logging.
- **`models/`**: Pre-trained machine learning weights.
  - `best_effnetb0_pytorch.pth`: EfficientNet-B0 weights for emotion recognition.
  - `career_prediction_model.joblib`: Random Forest classifier for career matching.
  - `feature_scaler.pkl`: StandardScaler for feature normalization.
- **`data/`**: Training datasets (e.g., `dataset.csv`).
- **`Module_Training/`**: Research and development notebooks for training the models.

## 🛠️ Requirements

The system requires Python 3.10+ and several AI libraries:
- **Web**: FastAPI, Uvicorn, WebSockets.
- **AI/ML**: PyTorch, Timm, Scikit-Learn, Joblib.
- **Data**: Pandas, NumPy, Matplotlib, Seaborn.
- **Imaging**: OpenCV, Pillow.

Install via: `pip install -r requirements.txt`

## 🚀 Execution

Run the backend from the `backend/` directory:
```powershell
python app.py
```
