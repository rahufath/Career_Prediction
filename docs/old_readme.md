# 🎯 AI Career Guidance System

An intelligent career recommendation system that predicts IT careers based on emotional patterns and personality traits using machine learning.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)

## 📋 Overview

This system uses machine learning to analyze your emotional responses and Big Five personality traits to recommend optimal IT career paths. It includes:

- **5 Personality Prediction Models** - Predicts Big Five traits from emotions
- **3 Career Prediction Models** - Random Forest, Gradient Boosting, Neural Network
- **15 IT Career Categories** - From Data Scientist to IT Project Manager
- **Interactive Web Interface** - Built with Streamlit
- **Natural Language Explanations** - Understand why careers are recommended

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Career Guidance System                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   Emotions   │───▶│  Personality │───▶│ Career Prediction │  │
│  │  (7 values)  │    │  Prediction  │    │   (15 classes)    │  │
│  └──────────────┘    │  (5 traits)  │    └──────────────────┘  │
│                      └──────────────┘                           │
│                                                                  │
│  Input Features: 18 (7 emotions + 5 personality + 6 engineered) │
│  Output: Career recommendation with confidence & explanation     │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Train models
python train_career_model.py

# Run web interface
streamlit run app.py
```

### API Usage

```python
from career_predictor import CareerPredictor

predictor = CareerPredictor()

# Predict from emotions
emotions = {
    'angry': 0.05, 'disgust': 0.02, 'fear': 0.03,
    'happy': 0.35, 'sad': 0.02, 'surprise': 0.08, 'neutral': 0.45
}
result = predictor.predict_career(emotions=emotions)
print(result['predicted_career'])  # "Data Scientist"

# Predict from personality
personality = {
    'openness': 0.85, 'conscientiousness': 0.75,
    'extraversion': 0.40, 'agreeableness': 0.60, 'neuroticism': 0.30
}
result = predictor.predict_career(personality=personality)
```

## 📊 Model Performance

| Model | Accuracy |
|-------|----------|
| Random Forest | ~78% |
| Gradient Boosting | ~75% |
| Neural Network | ~72% |

### Personality Prediction (R² Scores)
- Openness: ~0.45
- Conscientiousness: ~0.50
- Extraversion: ~0.55
- Agreeableness: ~0.48
- Neuroticism: ~0.52

## 💼 Career Categories

1. Data Scientist
2. Software Developer
3. DevOps Engineer
4. UI/UX Designer
5. Cybersecurity Analyst
6. Cloud Architect
7. Machine Learning Engineer
8. Full Stack Developer
9. Database Administrator
10. Network Engineer
11. Product Manager
12. Technical Writer
13. Quality Assurance Engineer
14. Systems Analyst
15. IT Project Manager

## 📁 Project Structure

```
├── train_career_model.py   # Training pipeline
├── career_predictor.py     # Prediction API
├── app.py                  # Streamlit web interface
├── demo.py                 # Interactive demos
├── requirements.txt        # Dependencies
├── dataset.csv             # Training data
├── models/                 # Saved models
│   ├── random_forest_model.pkl
│   ├── gradient_boosting_model.pkl
│   ├── neural_network_model.pkl
│   ├── personality_*_model.pkl
│   ├── feature_scaler.pkl
│   ├── label_encoder.pkl
│   └── metadata.json
├── model_comparison.png    # Accuracy comparison chart
└── confusion_matrix.png    # Confusion matrix visualization
```

## 🔧 API Reference

### CareerPredictor Class

```python
class CareerPredictor:
    def __init__(self, model_dir='models')
    def calculate_emotion_features(emotions: dict) -> dict
    def predict_personality_from_emotions(emotion_features: dict) -> dict
    def predict_career(emotions=None, personality=None, model_name='random_forest') -> dict
    def explain_prediction(personality: dict, career: str) -> str
    def get_available_models() -> list
    def get_careers() -> list
```

### Prediction Result Format

```python
{
    'predicted_career': 'Data Scientist',
    'top_careers': [
        {'career': 'Data Scientist', 'confidence': 0.78},
        {'career': 'Machine Learning Engineer', 'confidence': 0.65},
        ...
    ],
    'personality': {
        'openness': 0.82,
        'conscientiousness': 0.75,
        'extraversion': 0.45,
        'agreeableness': 0.60,
        'neuroticism': 0.32
    },
    'model_used': 'random_forest'
}
```

## 🚢 Deployment

### Local Development
```bash
streamlit run app.py
```

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python train_career_model.py
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

### Cloud Platforms
- **Streamlit Cloud**: Push to GitHub, connect to Streamlit Cloud
- **Heroku**: Add Procfile with `web: streamlit run app.py`
- **AWS/GCP**: Deploy as containerized application

## 🔬 Feature Engineering

| Feature | Calculation |
|---------|-------------|
| dominant_emotion_idx | argmax(emotions) |
| emotion_entropy | -Σ(p × log(p)) |
| emotion_variance | var(emotions) |
| neutral_ratio | neutral emotion value |
| positive_ratio | happy + surprise |
| negative_ratio | angry + disgust + fear + sad |

## 📝 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

---

Built with ❤️ using Python, scikit-learn, and Streamlit
