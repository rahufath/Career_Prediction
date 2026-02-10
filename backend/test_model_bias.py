import sys
import os
import json
# Add current directory to path so we can import app
sys.path.append(os.getcwd())

from app.services.career_service import CareerService

# Mock logger
import logging
logging.basicConfig(level=logging.INFO)

def test_bias():
    print("Initializing CareerService...")
    try:
        service = CareerService()
    except Exception as e:
        print(f"Failed to init service: {e}")
        return

    with open('bias_results.txt', 'w') as f:
        # Test Case 1: Happy
        emotions_happy = {'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 1.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}
        f.write("\nTest 1: Happy\n")
        res1 = service.predict_career(emotions=emotions_happy)
        f.write(f"Prediction: {res1['predicted_career']}\n")
        f.write(f"Top 3: {[c['career'] for c in res1['top_careers']]}\n")
        
        # Test Case 2: Sad/Fear
        emotions_sad = {'angry': 0.0, 'disgust': 0.0, 'fear': 0.5, 'happy': 0.0, 'sad': 0.5, 'surprise': 0.0, 'neutral': 0.0}
        f.write("\nTest 2: Sad/Fear\n")
        res2 = service.predict_career(emotions=emotions_sad)
        f.write(f"Prediction: {res2['predicted_career']}\n")
        f.write(f"Top 3: {[c['career'] for c in res2['top_careers']]}\n")
        
        # Test Case 3: Neutral/Conscientious
        emotions_neutral = {'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 1.0}
        f.write("\nTest 3: Neutral\n")
        res3 = service.predict_career(emotions=emotions_neutral)
        f.write(f"Prediction: {res3['predicted_career']}\n")
        f.write(f"Top 3: {[c['career'] for c in res3['top_careers']]}\n")

        # Test Case 4: Default / Empty (Simulating aggregation fallback)
        # aggregate_emotions returns: {'angry': 0.1, 'disgust': 0.05, 'fear': 0.1, 'happy': 0.3, 'sad': 0.1, 'surprise': 0.1, 'neutral': 0.25}
        emotions_default = {'angry': 0.1, 'disgust': 0.05, 'fear': 0.1, 'happy': 0.3, 'sad': 0.1, 'surprise': 0.1, 'neutral': 0.25}
        f.write("\nTest 4: Default Fallback\n")
        res4 = service.predict_career(emotions=emotions_default)
        f.write(f"Prediction: {res4['predicted_career']}\n")
        f.write(f"Top 3: {[c['career'] for c in res4['top_careers']]}\n")

if __name__ == "__main__":
    test_bias()
