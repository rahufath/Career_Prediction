import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def run_test(name, func):
    print(f"Testing {name}...", end=" ")
    try:
        func()
        print("✅ PASS")
        return True
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_health():
    resp = requests.get(f"{BASE_URL}/api/health")
    resp.raise_for_status()
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["predictor_loaded"] is True

def test_questions():
    resp = requests.get(f"{BASE_URL}/api/questions")
    resp.raise_for_status()
    data = resp.json()
    assert "questions" in data
    assert len(data["questions"]) == 10
    q1 = data["questions"][0]
    assert "id" in q1
    assert "question" in q1
    assert "category" in q1

def test_analyze():
    # Mocking 10 questions worth of emotion data
    # Simulating a user who is mostly happy/neutral/open
    emotion_history = []
    
    # Create valid payload structure
    for i in range(1, 11):
        emotion_history.append({
            "questionId": i,
            "emotions": {
                "angry": 0.0,
                "disgust": 0.0,
                "fear": 0.05,
                "happy": 0.6,
                "sad": 0.0,
                "surprise": 0.1,
                "neutral": 0.25
            },
            "timestamp": "2024-01-01T12:00:00Z"
        })

    payload = {
        "userName": "Test User",
        "emotionHistory": emotion_history
    }

    resp = requests.post(f"{BASE_URL}/api/analyze", json=payload)
    if resp.status_code != 200:
        print(f"\nResponse: {resp.text}")
    resp.raise_for_status()
    
    data = resp.json()
    
    # Check structure
    assert data["userName"] == "Test User"
    assert "personality" in data
    assert "topCareers" in data
    assert len(data["topCareers"]) >= 1
    assert "insights" in data
    
    # Check logic (happy user should be open/extraverted)
    # This might vary based on the model, but let's check basic structure types
    assert isinstance(data["personality"]["openness"], float)
    assert isinstance(data["topCareers"][0]["confidence"], float)

if __name__ == "__main__":
    print(f"Running Backend Tests against {BASE_URL}\n")
    
    tests = [
        ("Health Check", test_health),
        ("Get Questions", test_questions),
        ("Analyze Interview", test_analyze)
    ]
    
    passed = 0
    for name, func in tests:
        if run_test(name, func):
            passed += 1
            
    print(f"\nSummary: {passed}/{len(tests)} Tests Passed")
    if passed != len(tests):
        sys.exit(1)
