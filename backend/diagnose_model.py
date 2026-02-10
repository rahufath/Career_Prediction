from career_predictor import CareerPredictor
import numpy as np

def test_model():
    predictor = CareerPredictor(model_dir='models')
    
    test_scenarios = [
        {
            "name": "High Neutral (Standard composed candidate)",
            "emotions": {'angry': 0.05, 'disgust': 0.02, 'fear': 0.03, 'happy': 0.1, 'sad': 0.05, 'surprise': 0.05, 'neutral': 0.7}
        },
        {
            "name": "High Happy (Energetic candidate)",
            "emotions": {'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.8, 'sad': 0.0, 'surprise': 0.1, 'neutral': 0.1}
        },
        {
            "name": "High Fear/Stress (Anxious candidate)",
            "emotions": {'angry': 0.05, 'disgust': 0.05, 'fear': 0.6, 'happy': 0.0, 'sad': 0.1, 'surprise': 0.1, 'neutral': 0.1}
        },
        {
            "name": "Balanced/Mixed",
            "emotions": {'angry': 0.1, 'disgust': 0.1, 'fear': 0.1, 'happy': 0.2, 'sad': 0.1, 'surprise': 0.2, 'neutral': 0.2}
        },
        {
            "name": "Default Fallback (from main.py)",
            "emotions": {'angry': 0.1, 'disgust': 0.05, 'fear': 0.1, 'happy': 0.3, 'sad': 0.1, 'surprise': 0.1, 'neutral': 0.25}
        },
        {
            "name": "Angry/Frustrated",
            "emotions": {'angry': 0.7, 'disgust': 0.1, 'fear': 0.0, 'happy': 0.0, 'sad': 0.1, 'surprise': 0.0, 'neutral': 0.1}
        }
    ]

    print(f"{'Scenario':<40} | {'Predicted Career':<25} | {'Confidence':<10}")
    print("-" * 80)
    
    with open("diagnostic_results.txt", "w") as f:
        # Test standard scenarios with default model (Random Forest)
        f.write("=== STANDARD SCENARIOS (Random Forest) ===\n")
        for scenario in test_scenarios:
            result = predictor.predict_career(emotions=scenario["emotions"])
            career = result['predicted_career']
            conf = result['top_careers'][0]['confidence']
            personality = result['personality']
            
            f.write(f"Scenario: {scenario['name']}\n")
            f.write(f"Prediction: {career} ({conf:.2%})\n")
            f.write("Personality Traits:\n")
            for trait, score in personality.items():
                f.write(f"  - {trait}: {score:.2f}\n")
            f.write("-" * 30 + "\n")
            
        # Test models for Neutral scenario
        f.write("\n=== MODEL COMPARISON (High Neutral) ===\n")
        neutral_emotions = {'angry': 0.05, 'disgust': 0.02, 'fear': 0.03, 'happy': 0.1, 'sad': 0.05, 'surprise': 0.05, 'neutral': 0.7}
        for model in ['random_forest', 'gradient_boosting', 'neural_network', 'ensemble']:
            try:
                result = predictor.predict_career(emotions=neutral_emotions, model_name=model)
                career = result['predicted_career']
                conf = result['top_careers'][0]['confidence']
                f.write(f"Model: {model}\n")
                f.write(f"Prediction: {career} ({conf:.2%})\n")
                f.write("Top 3:\n")
                for c in result['top_careers'][:3]:
                    f.write(f"  - {c['career']}: {c['confidence']:.1%}\n")
                f.write("-" * 30 + "\n")
            except Exception as e:
                f.write(f"Model: {model} - Error: {e}\n")
    print("Results saved to diagnostic_results.txt")

if __name__ == "__main__":
    test_model()
