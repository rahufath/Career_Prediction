import os
import json
import numpy as np
import joblib
from typing import Dict, List, Optional, Tuple, Union
from ..utils.logger import get_logger
from ..schemas.constants import CAREER_DETAILS

logger = get_logger(__name__)

class CareerService:
    """
    Service for predicting careers from emotion and personality data.
    """
    
    EMOTION_NAMES = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    PERSONALITY_NAMES = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    ENGINEERED_NAMES = ['dominant_emotion_idx', 'emotion_entropy', 'emotion_variance',
                        'neutral_ratio', 'positive_ratio', 'negative_ratio']
    
    # Personality trait explanations
    TRAIT_EXPLANATIONS = {
        'openness': {
            'high': 'creative, curious, and open to new experiences',
            'medium': 'balanced between tradition and innovation',
            'low': 'practical, conventional, and detail-oriented'
        },
        'conscientiousness': {
            'high': 'organized, disciplined, and goal-oriented',
            'medium': 'balanced between flexibility and structure',
            'low': 'spontaneous, flexible, and adaptable'
        },
        'extraversion': {
            'high': 'outgoing, energetic, and social',
            'medium': 'ambivert with balanced social preferences',
            'low': 'introverted, reflective, and independent'
        },
        'agreeableness': {
            'high': 'cooperative, empathetic, and team-oriented',
            'medium': 'balanced between cooperation and independence',
            'low': 'analytical, objective, and straightforward'
        },
        'neuroticism': {
            'high': 'sensitive, detail-aware, and cautious',
            'medium': 'balanced emotional responsiveness',
            'low': 'calm, resilient, and stress-resistant'
        }
    }
    
    def __init__(self, model_dir: str = 'models'):
        self.model_dir = model_dir
        
        if not os.path.exists(model_dir):
            logger.error(f"Model directory not found: {model_dir}")
            raise FileNotFoundError(f"Model directory not found: {model_dir}")
        
        self._load_models()
        self._load_metadata()
        logger.info("CareerService initialized successfully")
    
    def _load_models(self) -> None:
        """Load all trained models from disk with robust error handling."""
        try:
            self.career_models = {}
            model_names = ['random_forest', 'gradient_boosting', 'neural_network']
            
            for name in model_names:
                path = os.path.join(self.model_dir, f'{name}_model.pkl')
                if os.path.exists(path):
                    try:
                        self.career_models[name] = joblib.load(path)
                        logger.info(f"Loaded career model: {name}")
                    except Exception as e:
                        logger.error(f"Failed to load career model {name}: {str(e)}")
                else:
                    logger.warning(f"Career model file missing: {path}")
            
            self.personality_models = {}
            for trait in self.PERSONALITY_NAMES:
                path = os.path.join(self.model_dir, f'personality_{trait}_model.pkl')
                if os.path.exists(path):
                    try:
                        self.personality_models[trait] = joblib.load(path)
                    except Exception as e:
                        logger.error(f"Failed to load personality model for {trait}: {str(e)}")
                else:
                    logger.warning(f"Personality model file missing for {trait}")
            
            emotion_scaler_path = os.path.join(self.model_dir, 'personality_emotion_scaler_model.pkl')
            if os.path.exists(emotion_scaler_path):
                self.emotion_scaler = joblib.load(emotion_scaler_path)
            else:
                self.emotion_scaler = None
                logger.warning("Personality emotion scaler missing")
            
            scaler_path = os.path.join(self.model_dir, 'feature_scaler.pkl')
            encoder_path = os.path.join(self.model_dir, 'label_encoder.pkl')
            
            if os.path.exists(scaler_path) and os.path.exists(encoder_path):
                self.scaler = joblib.load(scaler_path)
                self.label_encoder = joblib.load(encoder_path)
                logger.info("Core preprocessing models loaded")
            else:
                logger.error("Core scaler or encoder missing. Prediction will fail.")
                raise FileNotFoundError("Critical model files (scaler/encoder) missing")
                
        except Exception as e:
            logger.error(f"Critical failure during model loading: {str(e)}")
            raise
    
    def _load_metadata(self) -> None:
        """Load model metadata from JSON file."""
        metadata_path = os.path.join(self.model_dir, 'metadata.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load metadata: {str(e)}")
                self._generate_default_metadata()
        else:
            self._generate_default_metadata()

    def _generate_default_metadata(self) -> None:
        """Generate safe default metadata if file is missing or corrupted."""
        self.metadata = {
            'careers': list(self.label_encoder.classes_) if hasattr(self, 'label_encoder') else [],
            'n_features': 18,
            'n_classes': len(self.label_encoder.classes_) if hasattr(self, 'label_encoder') else 0
        }

    def calculate_emotion_features(self, emotions: Dict[str, float]) -> Dict[str, float]:
        emotion_values = np.array([
            emotions.get('angry', 0.0),
            emotions.get('disgust', 0.0),
            emotions.get('fear', 0.0),
            emotions.get('happy', 0.0),
            emotions.get('sad', 0.0),
            emotions.get('surprise', 0.0),
            emotions.get('neutral', 0.0)
        ])
        
        if emotion_values.sum() > 0:
            emotion_values = emotion_values / emotion_values.sum()
        else:
            emotion_values = np.array([0, 0, 0, 0, 0, 0, 1])
        
        dominant_emotion_idx = int(np.argmax(emotion_values))
        emotion_entropy = float(-np.sum(emotion_values * np.log(emotion_values + 1e-10)))
        emotion_variance = float(np.var(emotion_values))
        neutral_ratio = float(emotion_values[6])
        positive_ratio = float(emotion_values[3] + emotion_values[5])
        negative_ratio = float(emotion_values[0] + emotion_values[1] + emotion_values[2] + emotion_values[4])
        
        return {
            'angry': float(emotion_values[0]),
            'disgust': float(emotion_values[1]),
            'fear': float(emotion_values[2]),
            'happy': float(emotion_values[3]),
            'sad': float(emotion_values[4]),
            'surprise': float(emotion_values[5]),
            'neutral': float(emotion_values[6]),
            'dominant_emotion_idx': dominant_emotion_idx,
            'emotion_entropy': emotion_entropy,
            'emotion_variance': emotion_variance,
            'neutral_ratio': neutral_ratio,
            'positive_ratio': positive_ratio,
            'negative_ratio': negative_ratio
        }

    def predict_personality(self, emotion_features: Dict[str, float]) -> Dict[str, float]:
        feature_names = self.EMOTION_NAMES + self.ENGINEERED_NAMES
        X = np.array([[emotion_features[name] for name in feature_names]])
        
        if self.emotion_scaler is not None:
            X = self.emotion_scaler.transform(X)
        
        personality = {}
        has_models = False
        for trait in self.PERSONALITY_NAMES:
            if trait in self.personality_models:
                score = self.personality_models[trait].predict(X)[0]
                personality[trait] = float(np.clip(score, 0, 1))
                has_models = True
        
        # If no ML models loaded, derive personality from emotions using
        # psychology-based heuristics so the radar chart shows realistic,
        # varied results instead of a flat 0.5 pentagon.
        if not has_models:
            happy = emotion_features.get('happy', 0)
            sad = emotion_features.get('sad', 0)
            angry = emotion_features.get('angry', 0)
            fear = emotion_features.get('fear', 0)
            surprise = emotion_features.get('surprise', 0)
            neutral = emotion_features.get('neutral', 0)
            disgust = emotion_features.get('disgust', 0)
            positive_ratio = emotion_features.get('positive_ratio', happy + surprise)
            negative_ratio = emotion_features.get('negative_ratio', angry + sad + fear + disgust)
            emotion_variance = emotion_features.get('emotion_variance', 0)

            # Openness: correlated with surprise, emotional range, curiosity
            personality['openness'] = float(np.clip(
                0.45 + surprise * 0.8 + emotion_variance * 2.0 + happy * 0.15 - neutral * 0.2, 0.1, 0.95
            ))

            # Conscientiousness: correlated with low impulsivity, emotional stability
            personality['conscientiousness'] = float(np.clip(
                0.50 + neutral * 0.4 - angry * 0.5 - surprise * 0.2 + fear * 0.15, 0.1, 0.95
            ))

            # Extraversion: correlated with happiness, positive affect, expressiveness
            personality['extraversion'] = float(np.clip(
                0.35 + happy * 0.7 + surprise * 0.3 + positive_ratio * 0.3 - sad * 0.4 - neutral * 0.15, 0.1, 0.95
            ))

            # Agreeableness: correlated with happiness, low anger, empathy
            personality['agreeableness'] = float(np.clip(
                0.45 + happy * 0.5 - angry * 0.7 - disgust * 0.4 + sad * 0.1 + fear * 0.1, 0.1, 0.95
            ))

            # Neuroticism: correlated with negative emotions, emotional reactivity
            personality['neuroticism'] = float(np.clip(
                0.30 + fear * 0.6 + sad * 0.5 + angry * 0.4 + negative_ratio * 0.3 - happy * 0.3 - neutral * 0.2, 0.1, 0.95
            ))

            logger.info(f"Personality derived from emotion heuristics: {personality}")
        
        return personality

    def predict_career(
        self,
        emotions: Optional[Dict[str, float]] = None,
        personality: Optional[Dict[str, float]] = None,
        model_name: str = 'ensemble'
    ) -> Dict:
        if emotions is None and personality is None:
            raise ValueError("Must provide either emotions or personality")
        
        emotion_features = self.calculate_emotion_features(emotions) if emotions else None
        
        if personality is None:
            if emotion_features is None: raise ValueError("Cannot predict personality without emotions")
            personality = self.predict_personality(emotion_features)
        
        # Default features if none provided
        if emotion_features is None:
            emotion_features = {
                'angry': 0.05, 'disgust': 0.05, 'fear': 0.05, 'happy': 0.3, 'sad': 0.05, 'surprise': 0.1, 'neutral': 0.4,
                'dominant_emotion_idx': 3, 'emotion_entropy': 1.5, 'emotion_variance': 0.02,
                'neutral_ratio': 0.4, 'positive_ratio': 0.4, 'negative_ratio': 0.2
            }
        
        
        feature_vector = [
            emotion_features['angry'], emotion_features['disgust'], emotion_features['fear'],
            emotion_features['happy'], emotion_features['sad'], emotion_features['surprise'],
            emotion_features['neutral'], personality['openness'], personality['conscientiousness'],
            personality['extraversion'], personality['agreeableness'], personality['neuroticism'],
            emotion_features['dominant_emotion_idx'], emotion_features['emotion_entropy'],
            emotion_features['emotion_variance'], emotion_features['neutral_ratio'],
            emotion_features['positive_ratio'], emotion_features['negative_ratio']
        ]
        
        X_scaled = self.scaler.transform(np.array([feature_vector]))
        
        available_models = list(self.career_models.keys())
        
        if model_name == 'ensemble' and available_models:
            all_probs = [self.career_models[m].predict_proba(X_scaled)[0] for m in available_models]
            probabilities = np.mean(all_probs, axis=0)
            model_info = f"ensemble({', '.join(available_models)})"
        else:
            m_name = model_name if model_name in self.career_models else available_models[0]
            probabilities = self.career_models[m_name].predict_proba(X_scaled)[0]
            model_info = m_name

        prediction = np.argmax(probabilities)
        predicted_career = self.label_encoder.classes_[prediction]
        
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_careers = []
        for idx in top_indices:
            career_name = self.label_encoder.classes_[idx]
            confidence = float(probabilities[idx])
            top_careers.append({
                'career': career_name,
                'confidence': confidence,
                'justification': self.generate_justification(career_name, personality, emotion_features)
            })
        
        return {
            'predicted_career': predicted_career,
            'top_careers': top_careers,
            'personality': personality,
            'model_used': model_info
        }

    def generate_justification(self, career: str, personality: Dict[str, float], emotions: Dict[str, float]) -> str:
        """Generate a personalized reasoning for a career recommendation."""
        traits = []
        if personality.get('openness', 0) > 0.6: traits.append("creative curiosity")
        if personality.get('conscientiousness', 0) > 0.6: traits.append("methodical discipline")
        if personality.get('extraversion', 0) > 0.6: traits.append("interpersonal energy")
        if personality.get('agreeableness', 0) > 0.6: traits.append("empathetic collaboration")
        if personality.get('neuroticism', 0) < 0.4: traits.append("stable composure")
        
        # Filter for only standard emotions to find the true dominant one
        valid_emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        filtered_emotions = {k: v for k, v in emotions.items() if k in valid_emotions}
        
        if filtered_emotions:
            dominant_emotion = max(filtered_emotions.items(), key=lambda x: x[1])[0]
        else:
            dominant_emotion = "focused"
        
        reason = f"Matches your {', '.join(traits[:2]) if traits else 'versatile cognitive profile'}."
        reason += f" Your steady {dominant_emotion} focus suggests high suitability for {career}."
        
        return reason

    def get_careers(self) -> List[str]:
        return list(self.label_encoder.classes_)
