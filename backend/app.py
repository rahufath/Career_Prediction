"""
AI Career Interview System - FastAPI Backend
=============================================
REST API for emotion analysis, personality prediction, and career recommendations.
Version: 2.1.0 (Modular)
"""

import logging

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import asyncio

# Import modular components
from service.api_models import AnalyzeRequest, AnalyzeResponse, CareerRecommendation, PersonalityResult, WSMessage
from service.constants import INTERVIEW_QUESTIONS, CAREER_DETAILS
from service.career_guide_service import CareerService
from lib.analysis_helpers import aggregate_emotions, generate_insights
from lib.logger import get_logger

# Initialize professional logger
logger = get_logger(__name__)

app = FastAPI(
    title="AI Career Interview System",
    description="Professional API for emotion-based career recommendations",
    version="2.1.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize career service
try:
    career_service = CareerService(model_dir="models")
    logger.info("[DONE] Career Service initialized and models loaded")
except Exception as e:
    logger.error(f"Failed to initialize Career Service: {str(e)}")
    career_service = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "AI Career Interview System API",
        "version": "2.1.0"
    }

@app.get("/api/questions")
async def get_questions():
    """Return all interview questions."""
    logger.info("Fetching interview questions")
    return {"questions": INTERVIEW_QUESTIONS}

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_interview(request: AnalyzeRequest):
    """
    Analyze interview session data:
    1. Aggregates emotional history
    2. Predicts personality traits
    3. Recommends careers using the Random Forest model
    """
    if not career_service:
        logger.error("Attempted analysis but Career Service is not available")
        raise HTTPException(status_code=503, detail="Career recommendation service is unavailable")

    try:
        logger.info(f"Analyzing session for user: {request.userName}")
        
        # 1. Aggregate emotions
        aggregated = aggregate_emotions(request.emotionHistory)
        
        # 2. Predict career using the Random Forest model
        result = career_service.predict_career(emotions=aggregated)
        
        personality = result['personality']
        top_career = result['predicted_career']
        
        # 3. Create recommendations list
        top_careers_data = []
        other_careers_data = []
        
        for i, item in enumerate(result['top_careers']):
            details = CAREER_DETAILS.get(item['career'], {})
            rec = CareerRecommendation(
                career=item['career'],
                confidence=item['confidence'],
                description=details.get('description', "A rewarding career path in technology."),
                skills=details.get('skills', []),
                growth_path=details.get('growth_path'),
                justification=item.get('justification')
            )
            if i == 0:
                top_careers_data.append(rec)
            else:
                other_careers_data.append(rec)
        
        # 4. Generate insights
        insights = generate_insights(personality, top_career, aggregated)
        
        # 5. Format emotion timeline
        timeline = [
            {"time": item.timestamp if item.timestamp else f"Q{item.questionId}", "emotions": item.emotions.model_dump()}
            for item in request.emotionHistory
        ]
        
        response = AnalyzeResponse(
            userName=request.userName,
            aggregatedEmotions=aggregated,
            personality=PersonalityResult(**personality),
            topCareers=top_careers_data,
            otherCareers=other_careers_data,
            emotionTimeline=timeline,
            insights=insights,
            blinkRate=request.blinkRate
        )
        
        logger.info(f"Analysis complete for user: {request.userName}. Predicted: {top_career}")
        return response
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    """
    Real-time WebSocket endpoint for streaming emotion data.
    Provides live feedback on confidence and dominant emotions.
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    # Optimized: Use running totals for O(1) aggregation
    STANDARD_EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    session_sums = {k: 0.0 for k in STANDARD_EMOTIONS}
    session_count = 0
    
    try:
        while True:
            # Receive data from frontend
            data = await websocket.receive_text()
            
            try:
                # 1. Validate incoming data structure
                message = WSMessage.model_validate_json(data)
                
                # 2. Update session history from validated data
                new_emotions = message.emotions
                if new_emotions:
                    emo_dict = new_emotions.model_dump()
                    for k in STANDARD_EMOTIONS:
                        session_sums[k] += emo_dict.get(k, 0.0)
                    session_count += 1
                
                # 3. Handle optional image frame
                image_frame = message.image
                try:
                    if image_frame and career_service:
                        backend_emotions = career_service.predict_emotion(image_frame)
                        for k in STANDARD_EMOTIONS:
                            session_sums[k] += backend_emotions.get(k, 0.0)
                        session_count += 1
    
                        # 3. Fast O(1) aggregation
                        current_aggregated = {
                            k: (session_sums[k] / session_count)
                            for k in STANDARD_EMOTIONS
                        }
                        
                        # 4. Predict career (Offload to thread pool for responsiveness)
                        loop = asyncio.get_event_loop()
                        prediction = await loop.run_in_executor(
                            None, 
                            lambda: career_service.predict_career(emotions=current_aggregated)
                        )
                        
                        # 6. Send live feedback
                        await websocket.send_json({
                            "type": "LIVE_INSIGHT",
                            "topCareer": prediction['predicted_career'],
                            "confidence": prediction['top_careers'][0]['confidence'],
                            "dominantEmotion": max(current_aggregated.items(), key=lambda x: x[1])[0],
                            "personality": prediction['personality']
                        })
                except Exception as e:
                    logger.error(f"Prediction error in WebSocket loop: {str(e)}")
                    await websocket.send_json({"error": "Internal prediction error", "detail": str(e)})
            
            except Exception as e:
                logger.warning(f"Invalid message format received: {str(e)}")
                await websocket.send_json({"error": "Invalid format", "detail": "Data did not match expected schema"})
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        try:
            await websocket.close()
        except:
            pass

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    logger.info("Shutting down application...")

if __name__ == "__main__":
    import uvicorn
    import sys
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")
    except OSError as e:
        if "[WinError 10048]" in str(e) or e.errno == 10048:
            print("\n\n" + "="*60)
            print("ERROR: Port 8000 is already in use!")
            print("Another instance of the backend is likely running.")
            print("Please close it (Ctrl+C) or kill it via Task Manager.")
            print("="*60 + "\n")
            sys.exit(1)
        else:
            raise e
