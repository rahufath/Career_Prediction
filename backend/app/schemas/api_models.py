from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional

class Question(BaseModel):
    id: int
    question: str
    category: str
    duration: int

class EmotionData(BaseModel):
    angry: float = Field(0.0, ge=0.0, le=1.0)
    disgust: float = Field(0.0, ge=0.0, le=1.0)
    fear: float = Field(0.0, ge=0.0, le=1.0)
    happy: float = Field(0.0, ge=0.0, le=1.0)
    sad: float = Field(0.0, ge=0.0, le=1.0)
    surprise: float = Field(0.0, ge=0.0, le=1.0)
    neutral: float = Field(0.0, ge=0.0, le=1.0)

class QuestionEmotions(BaseModel):
    questionId: int
    emotions: EmotionData
    timestamp: Optional[str] = None

class AnalyzeRequest(BaseModel):
    userName: str = Field(..., min_length=2, max_length=50)
    emotionHistory: List[QuestionEmotions]
    blinkRate: Optional[float] = None

    @validator('userName')
    def name_must_be_alphabetic(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('User name must only contain letters and spaces')
        return v

class PersonalityResult(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

class CareerRecommendation(BaseModel):
    career: str
    confidence: float
    description: str
    skills: List[str] = []
    growth_path: Optional[str] = None
    justification: Optional[str] = None

class AnalyzeResponse(BaseModel):
    userName: str
    aggregatedEmotions: Dict[str, float]
    personality: PersonalityResult
    topCareers: List[CareerRecommendation]
    otherCareers: List[CareerRecommendation]
    emotionTimeline: List[Dict]
    insights: List[str]
    blinkRate: Optional[float] = None
