"""
AI Career Guidance System - Training Pipeline
==============================================
Trains ML models to predict IT careers from emotion and personality data.

Features:
- Generates synthetic dataset (495 samples, 15 careers)
- Trains 5 personality prediction models (GradientBoosting)
- Trains 3 career prediction models (RF, GB, MLP)
- Generates evaluation visualizations
- Saves all models and metadata

Author: AI Career Guidance System
Version: 1.0.0
"""

import os
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    mean_squared_error, mean_absolute_error, r2_score
)
import joblib

warnings.filterwarnings('ignore')

# Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_DIR = 'models'

# 15 IT Career Categories
CAREERS = [
    'Data Scientist',
    'Software Developer', 
    'DevOps Engineer',
    'UI/UX Designer',
    'Cybersecurity Analyst',
    'Cloud Architect',
    'Machine Learning Engineer',
    'Full Stack Developer',
    'Database Administrator',
    'Network Engineer',
    'Product Manager',
    'Technical Writer',
    'Quality Assurance Engineer',
    'Systems Analyst',
    'IT Project Manager'
]

# Career-personality profiles (ideal traits for each career) - DISTINCT profiles
CAREER_PROFILES = {
    # Creative/Open careers - high openness
    'Data Scientist': {'openness': 0.85, 'conscientiousness': 0.70, 'extraversion': 0.35, 'agreeableness': 0.55, 'neuroticism': 0.25},
    'Machine Learning Engineer': {'openness': 0.90, 'conscientiousness': 0.75, 'extraversion': 0.30, 'agreeableness': 0.50, 'neuroticism': 0.30},
    'UI/UX Designer': {'openness': 0.95, 'conscientiousness': 0.55, 'extraversion': 0.65, 'agreeableness': 0.80, 'neuroticism': 0.45},
    
    # Detail-oriented careers - high conscientiousness
    'Database Administrator': {'openness': 0.40, 'conscientiousness': 0.95, 'extraversion': 0.25, 'agreeableness': 0.50, 'neuroticism': 0.20},
    'Cybersecurity Analyst': {'openness': 0.50, 'conscientiousness': 0.90, 'extraversion': 0.25, 'agreeableness': 0.40, 'neuroticism': 0.20},
    'Quality Assurance Engineer': {'openness': 0.45, 'conscientiousness': 0.92, 'extraversion': 0.35, 'agreeableness': 0.60, 'neuroticism': 0.25},
    
    # Social/Leadership careers - high extraversion
    'Product Manager': {'openness': 0.70, 'conscientiousness': 0.70, 'extraversion': 0.90, 'agreeableness': 0.80, 'neuroticism': 0.35},
    'IT Project Manager': {'openness': 0.55, 'conscientiousness': 0.80, 'extraversion': 0.85, 'agreeableness': 0.75, 'neuroticism': 0.30},
    'Systems Analyst': {'openness': 0.60, 'conscientiousness': 0.75, 'extraversion': 0.70, 'agreeableness': 0.70, 'neuroticism': 0.30},
    
    # Technical/Independent careers - low extraversion
    'Software Developer': {'openness': 0.65, 'conscientiousness': 0.80, 'extraversion': 0.30, 'agreeableness': 0.55, 'neuroticism': 0.35},
    'Full Stack Developer': {'openness': 0.70, 'conscientiousness': 0.75, 'extraversion': 0.40, 'agreeableness': 0.60, 'neuroticism': 0.40},
    'Network Engineer': {'openness': 0.45, 'conscientiousness': 0.85, 'extraversion': 0.30, 'agreeableness': 0.45, 'neuroticism': 0.25},
    
    # Infrastructure/Ops careers - balanced
    'DevOps Engineer': {'openness': 0.60, 'conscientiousness': 0.85, 'extraversion': 0.45, 'agreeableness': 0.55, 'neuroticism': 0.25},
    'Cloud Architect': {'openness': 0.75, 'conscientiousness': 0.80, 'extraversion': 0.50, 'agreeableness': 0.55, 'neuroticism': 0.25},
    
    # Communication-focused - high agreeableness
    'Technical Writer': {'openness': 0.80, 'conscientiousness': 0.75, 'extraversion': 0.40, 'agreeableness': 0.85, 'neuroticism': 0.30}
}


def print_header(text: str, char: str = "=") -> None:
    """Print formatted header."""
    print(f"\n{char * 60}")
    print(f" {text}")
    print(f"{char * 60}\n")


def print_section(text: str) -> None:
    """Print formatted section header."""
    print(f"\n{'─' * 40}")
    print(f"  {text}")
    print(f"{'─' * 40}")


def generate_synthetic_dataset(n_samples: int = 495) -> pd.DataFrame:
    """
    Generate synthetic emotion-personality-career dataset.
    
    Args:
        n_samples: Total number of samples to generate
        
    Returns:
        DataFrame with emotions, personality traits, and career labels
    """
    print_section("Generating Synthetic Dataset")
    
    np.random.seed(RANDOM_STATE)
    samples_per_career = n_samples // len(CAREERS)
    
    data = []
    
    for career in CAREERS:
        profile = CAREER_PROFILES[career]
        
        for _ in range(samples_per_career):
            # Generate personality traits with minimal noise for distinct profiles
            personality = {
                trait: np.clip(profile[trait] + np.random.normal(0, 0.05), 0, 1)
                for trait in ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
            }
            
            # Generate emotions correlated with personality
            # High neuroticism -> more negative emotions
            # High extraversion -> more positive emotions
            # High openness -> more surprise
            base_emotions = np.array([0.1, 0.05, 0.1, 0.3, 0.1, 0.1, 0.25])  # angry, disgust, fear, happy, sad, surprise, neutral
            
            # Modulate based on personality
            neuro_factor = personality['neuroticism']
            extra_factor = personality['extraversion']
            open_factor = personality['openness']
            
            emotions = base_emotions.copy()
            emotions[0] += neuro_factor * 0.15  # angry
            emotions[1] += neuro_factor * 0.1   # disgust
            emotions[2] += neuro_factor * 0.15  # fear
            emotions[3] += extra_factor * 0.2   # happy
            emotions[4] += neuro_factor * 0.15  # sad
            emotions[5] += open_factor * 0.15   # surprise
            emotions[6] -= neuro_factor * 0.1   # neutral
            
            # Add reduced noise and normalize
            emotions += np.random.normal(0, 0.02, 7)
            emotions = np.clip(emotions, 0.01, 1)
            emotions = emotions / emotions.sum()
            
            # Calculate engineered features
            dominant_emotion_idx = np.argmax(emotions)
            emotion_entropy = -np.sum(emotions * np.log(emotions + 1e-10))
            emotion_variance = np.var(emotions)
            neutral_ratio = emotions[6]
            positive_ratio = emotions[3] + emotions[5]  # happy + surprise
            negative_ratio = emotions[0] + emotions[1] + emotions[2] + emotions[4]  # angry + disgust + fear + sad
            
            sample = {
                'angry': emotions[0],
                'disgust': emotions[1],
                'fear': emotions[2],
                'happy': emotions[3],
                'sad': emotions[4],
                'surprise': emotions[5],
                'neutral': emotions[6],
                'openness': personality['openness'],
                'conscientiousness': personality['conscientiousness'],
                'extraversion': personality['extraversion'],
                'agreeableness': personality['agreeableness'],
                'neuroticism': personality['neuroticism'],
                'dominant_emotion_idx': dominant_emotion_idx,
                'emotion_entropy': emotion_entropy,
                'emotion_variance': emotion_variance,
                'neutral_ratio': neutral_ratio,
                'positive_ratio': positive_ratio,
                'negative_ratio': negative_ratio,
                'matched_career': career
            }
            data.append(sample)
    
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    
    print(f"✓ Generated {len(df)} samples across {len(CAREERS)} careers")
    print(f"✓ Features: 7 emotions + 5 personality + 6 engineered = 18 total")
    
    return df


def exploratory_data_analysis(df: pd.DataFrame) -> None:
    """Perform and display exploratory data analysis."""
    print_section("Exploratory Data Analysis")
    
    print("\n📊 Dataset Shape:", df.shape)
    print("\n📋 Column Types:")
    print(df.dtypes.to_string())
    
    print("\n📈 Numerical Statistics:")
    print(df.describe().round(3).to_string())
    
    print("\n🎯 Career Distribution:")
    career_counts = df['matched_career'].value_counts()
    for career, count in career_counts.items():
        print(f"   {career}: {count} samples ({count/len(df)*100:.1f}%)")
    
    print("\n🔗 Feature Correlations (Top 5 with target):")
    # Encode career for correlation
    le_temp = LabelEncoder()
    df_temp = df.copy()
    df_temp['career_encoded'] = le_temp.fit_transform(df['matched_career'])
    
    correlations = df_temp.drop(['matched_career'], axis=1).corr()['career_encoded'].abs().sort_values(ascending=False)
    for feat, corr in correlations[1:6].items():
        print(f"   {feat}: {corr:.3f}")


def prepare_data(df: pd.DataFrame):
    """
    Prepare data for training.
    
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, scaler, label_encoder, feature_names)
    """
    print_section("Data Preparation")
    
    # Define features
    emotion_features = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    personality_features = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    engineered_features = ['dominant_emotion_idx', 'emotion_entropy', 'emotion_variance', 
                          'neutral_ratio', 'positive_ratio', 'negative_ratio']
    
    all_features = emotion_features + personality_features + engineered_features
    
    X = df[all_features].values
    y = df['matched_career'].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_encoded
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✓ Training samples: {len(X_train)}")
    print(f"✓ Testing samples: {len(X_test)}")
    print(f"✓ Features: {len(all_features)}")
    print(f"✓ Classes: {len(label_encoder.classes_)}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, label_encoder, all_features


def train_personality_models(df: pd.DataFrame):
    """
    Train models to predict Big Five personality from emotions.
    
    Returns:
        Dict of personality models and their metrics
    """
    print_section("Training Personality Prediction Models")
    
    emotion_features = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    engineered_features = ['dominant_emotion_idx', 'emotion_entropy', 'emotion_variance',
                          'neutral_ratio', 'positive_ratio', 'negative_ratio']
    personality_traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    
    X = df[emotion_features + engineered_features].values
    
    # Scale emotion features
    emotion_scaler = StandardScaler()
    X_scaled = emotion_scaler.fit_transform(X)
    
    personality_models = {}
    personality_metrics = {}
    
    for trait in personality_traits:
        y = df[trait].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        
        model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=RANDOM_STATE
        )
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        personality_models[trait] = model
        personality_metrics[trait] = {'r2': r2, 'mae': mae, 'rmse': rmse}
        
        status = "✓" if r2 > 0.3 else "○"
        print(f"  {status} {trait.capitalize():20s} R²={r2:.3f}, MAE={mae:.3f}, RMSE={rmse:.3f}")
    
    # Save emotion scaler
    personality_models['emotion_scaler'] = emotion_scaler
    
    return personality_models, personality_metrics


def train_career_models(X_train, X_test, y_train, y_test, label_encoder):
    """
    Train career prediction models.
    
    Returns:
        Dict of models and their metrics
    """
    print_section("Training Career Prediction Models")
    
    models = {
        'random_forest': RandomForestClassifier(
            n_estimators=300,
            max_depth=15,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),
        'gradient_boosting': GradientBoostingClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            random_state=RANDOM_STATE
        ),
        'neural_network': MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            max_iter=500,
            random_state=RANDOM_STATE,
            early_stopping=True
        )
    }
    
    trained_models = {}
    model_metrics = {}
    
    for name, model in models.items():
        print(f"\n  Training {name}...")
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        trained_models[name] = model
        model_metrics[name] = {
            'accuracy': accuracy,
            'y_pred': y_pred,
            'classification_report': classification_report(
                y_test, y_pred, 
                target_names=label_encoder.classes_,
                output_dict=True
            )
        }
        
        print(f"  ✓ {name}: Accuracy = {accuracy:.2%}")
    
    return trained_models, model_metrics


def evaluate_models(model_metrics, y_test, label_encoder):
    """Display detailed model evaluation."""
    print_section("Model Evaluation")
    
    # Find best model
    best_model = max(model_metrics.items(), key=lambda x: x[1]['accuracy'])
    print(f"\n🏆 Best Model: {best_model[0]} ({best_model[1]['accuracy']:.2%} accuracy)")
    
    # Print classification report for best model
    print(f"\n📊 Classification Report ({best_model[0]}):\n")
    report = model_metrics[best_model[0]]['classification_report']
    
    print(f"{'Career':<30} {'Precision':>10} {'Recall':>10} {'F1-Score':>10} {'Support':>10}")
    print("-" * 70)
    
    for career in label_encoder.classes_:
        if career in report:
            metrics = report[career]
            print(f"{career:<30} {metrics['precision']:>10.2f} {metrics['recall']:>10.2f} {metrics['f1-score']:>10.2f} {int(metrics['support']):>10}")
    
    print("-" * 70)
    print(f"{'Accuracy':<30} {'':<10} {'':<10} {report['accuracy']:>10.2f} {int(report['weighted avg']['support']):>10}")
    print(f"{'Macro Avg':<30} {report['macro avg']['precision']:>10.2f} {report['macro avg']['recall']:>10.2f} {report['macro avg']['f1-score']:>10.2f}")
    print(f"{'Weighted Avg':<30} {report['weighted avg']['precision']:>10.2f} {report['weighted avg']['recall']:>10.2f} {report['weighted avg']['f1-score']:>10.2f}")
    
    return best_model[0]


def plot_model_comparison(model_metrics, save_path: str = 'model_comparison.png'):
    """Create and save model accuracy comparison chart."""
    print_section("Generating Visualizations")
    
    models = list(model_metrics.keys())
    accuracies = [model_metrics[m]['accuracy'] * 100 for m in models]
    
    plt.figure(figsize=(10, 6))
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    bars = plt.bar(models, accuracies, color=colors, edgecolor='white', linewidth=2)
    
    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{acc:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Model', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.title('Career Prediction Model Comparison', fontsize=14, fontweight='bold')
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path}")


def plot_confusion_matrix(y_test, y_pred, label_encoder, save_path: str = 'confusion_matrix.png'):
    """Create and save confusion matrix heatmap."""
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=label_encoder.classes_,
                yticklabels=label_encoder.classes_)
    
    plt.xlabel('Predicted', fontsize=12)
    plt.ylabel('Actual', fontsize=12)
    plt.title('Confusion Matrix - Best Model', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {save_path}")


def save_models(career_models, personality_models, scaler, label_encoder, 
                feature_names, model_metrics, personality_metrics):
    """Save all models and metadata to disk."""
    print_section("Saving Models")
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save career models
    for name, model in career_models.items():
        path = os.path.join(MODEL_DIR, f'{name}_model.pkl')
        joblib.dump(model, path)
        print(f"  ✓ Saved: {path}")
    
    # Save personality models
    for trait, model in personality_models.items():
        path = os.path.join(MODEL_DIR, f'personality_{trait}_model.pkl')
        joblib.dump(model, path)
        print(f"  ✓ Saved: {path}")
    
    # Save preprocessing objects
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'feature_scaler.pkl'))
    print(f"  ✓ Saved: {MODEL_DIR}/feature_scaler.pkl")
    
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, 'label_encoder.pkl'))
    print(f"  ✓ Saved: {MODEL_DIR}/label_encoder.pkl")
    
    # Save metadata
    metadata = {
        'careers': list(label_encoder.classes_),
        'feature_names': feature_names,
        'n_features': len(feature_names),
        'n_classes': len(label_encoder.classes_),
        'model_accuracies': {k: v['accuracy'] for k, v in model_metrics.items()},
        'personality_metrics': personality_metrics,
        'emotion_features': ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'],
        'personality_features': ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'],
        'engineered_features': ['dominant_emotion_idx', 'emotion_entropy', 'emotion_variance',
                               'neutral_ratio', 'positive_ratio', 'negative_ratio']
    }
    
    with open(os.path.join(MODEL_DIR, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"  ✓ Saved: {MODEL_DIR}/metadata.json")


def main():
    """Main training pipeline."""
    print_header("AI CAREER GUIDANCE SYSTEM - TRAINING PIPELINE")
    
    # Step 1: Generate dataset
    df = generate_synthetic_dataset(990)
    
    # Save dataset
    df.to_csv('dataset.csv', index=False)
    print(f"  ✓ Saved: dataset.csv")
    
    # Step 2: Exploratory Data Analysis
    exploratory_data_analysis(df)
    
    # Step 3: Prepare data
    X_train, X_test, y_train, y_test, scaler, label_encoder, feature_names = prepare_data(df)
    
    # Step 4: Train personality prediction models
    personality_models, personality_metrics = train_personality_models(df)
    
    # Step 5: Train career prediction models
    career_models, model_metrics = train_career_models(X_train, X_test, y_train, y_test, label_encoder)
    
    # Step 6: Evaluate models
    best_model_name = evaluate_models(model_metrics, y_test, label_encoder)
    
    # Step 7: Generate visualizations
    plot_model_comparison(model_metrics, 'model_comparison.png')
    plot_confusion_matrix(y_test, model_metrics[best_model_name]['y_pred'], label_encoder, 'confusion_matrix.png')
    
    # Step 8: Save all models
    save_models(career_models, personality_models, scaler, label_encoder,
                feature_names, model_metrics, personality_metrics)
    
    # Final summary
    print_header("TRAINING COMPLETE", "★")
    print("📊 Results Summary:")
    print(f"   • Dataset: 990 samples, 15 careers")
    print(f"   • Best Model: {best_model_name}")
    print(f"   • Best Accuracy: {model_metrics[best_model_name]['accuracy']:.2%}")
    print(f"\n📁 Files Generated:")
    print(f"   • dataset.csv")
    print(f"   • model_comparison.png")
    print(f"   • confusion_matrix.png")
    print(f"   • models/ directory with {len(career_models) + len(personality_models) + 2} files")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Run: python demo.py")
    print(f"   2. Run: streamlit run app.py")


if __name__ == '__main__':
    main()
