# ⚡ Quick Start Guide

Get the AI Career Guidance System running in 5 minutes!

## 📦 Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- scikit-learn, pandas, numpy (ML)
- matplotlib, seaborn, plotly (Visualization)
- streamlit (Web interface)

## 🏋️ Step 2: Train Models

```bash
python train_career_model.py
```

This will:
- Generate synthetic dataset (495 samples)
- Train 5 personality prediction models
- Train 3 career prediction models
- Save everything to `models/` directory

Expected output:
```
✓ Generated 495 samples across 15 careers
✓ Training complete with ~75% accuracy
```

## 🌐 Step 3: Launch Web App

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## 🧪 Step 4: Try the Demo

```bash
python demo.py
```

Interactive demos:
1. Emotion-Based Prediction
2. Personality-Based Prediction
3. Combined Prediction
4. Model Comparison
5. Edge Cases

---

## 🎯 Quick Examples

### Example 1: Using the API

```python
from career_predictor import CareerPredictor

predictor = CareerPredictor()

# From emotions
result = predictor.predict_career(emotions={
    'happy': 0.4, 'neutral': 0.3, 'surprise': 0.15,
    'angry': 0.05, 'sad': 0.05, 'fear': 0.03, 'disgust': 0.02
})
print(f"Career: {result['predicted_career']}")
```

### Example 2: From Personality

```python
result = predictor.predict_career(personality={
    'openness': 0.8,
    'conscientiousness': 0.75,
    'extraversion': 0.5,
    'agreeableness': 0.6,
    'neuroticism': 0.3
})
```

---

## 🧠 Personality Traits Explained

| Trait | High Score | Low Score |
|-------|------------|-----------|
| **Openness** | Creative, curious | Practical, conventional |
| **Conscientiousness** | Organized, disciplined | Flexible, spontaneous |
| **Extraversion** | Outgoing, energetic | Reserved, independent |
| **Agreeableness** | Cooperative, empathetic | Analytical, objective |
| **Neuroticism** | Sensitive, cautious | Calm, resilient |

---

## 💼 Available Careers

| Technical | Leadership | Specialist |
|-----------|------------|------------|
| Software Developer | Product Manager | Data Scientist |
| Full Stack Developer | IT Project Manager | ML Engineer |
| DevOps Engineer | Systems Analyst | Cybersecurity Analyst |
| Database Admin | | UI/UX Designer |
| Network Engineer | | Technical Writer |
| Cloud Architect | | QA Engineer |

---

## ❓ Troubleshooting

### "Models not found" error
Run `python train_career_model.py` first.

### Import errors
Ensure all packages are installed: `pip install -r requirements.txt`

### Streamlit not starting
Check port 8501 is free or use `streamlit run app.py --server.port 8502`

---

## 🎓 Tips for Best Results

1. **Be honest** with emotion/personality inputs
2. **Try different models** - they may suggest different careers
3. **Read the explanation** - it provides valuable insights
4. **Consider top 5 careers** - not just the #1 recommendation
5. **Use Combined mode** for most comprehensive analysis

---

**Next Steps:**
- Explore `career_predictor.py` for API integration
- Read `README.md` for full documentation
- Check `PROJECT_SUMMARY.md` for technical details
