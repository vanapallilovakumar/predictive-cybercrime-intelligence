import os
import random
import joblib
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import HistGradientBoostingClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score

from backend.ml_pipeline.features import extract_record_features

WEIGHTS_DIR = os.path.join(os.path.dirname(__file__), "weights")
os.makedirs(WEIGHTS_DIR, exist_ok=True)

HOTSPOTS = [
    {"district": "Deoghar", "lat": 24.4854, "lon": 86.6978, "base_prob": 0.75},
    {"district": "Jamtara", "lat": 23.9620, "lon": 86.8020, "base_prob": 0.70},
    {"district": "Nuh", "lat": 28.1060, "lon": 77.0120, "base_prob": 0.70},
    {"district": "Bharatpur", "lat": 27.2170, "lon": 77.4895, "base_prob": 0.65},
    {"district": "Mathura", "lat": 27.4924, "lon": 77.6737, "base_prob": 0.40},
    {"district": "Giridih", "lat": 24.1840, "lon": 86.3050, "base_prob": 0.38}
]

TYPOLOGIES = ["otp fraud", "upi fraud", "digital arrest", "job fraud", "investment scam", "loan app extortion"]

def generate_synthetic_dataset(n_samples: int = 600):
    X = []
    y = []
    random.seed(42)
    np.random.seed(42)
    
    base_time = datetime.now()
    
    for _ in range(n_samples):
        hotspot = random.choice(HOTSPOTS)
        typology = random.choice(TYPOLOGIES)
        
        lat = hotspot["lat"] + random.uniform(-0.05, 0.05)
        lon = hotspot["lon"] + random.uniform(-0.05, 0.05)
        
        hours_offset = random.randint(0, 30 * 24)
        ts = base_time - timedelta(hours=hours_offset)
        
        if typology in ("investment scam", "digital arrest"):
            loss = random.uniform(150000, 1000000)
        else:
            loss = random.uniform(10000, 200000)
            
        record = {
            "loss_amount_inr": loss,
            "typology": typology,
            "incident_timestamp": ts.isoformat(),
            "latitude": lat,
            "longitude": lon,
            "district": hotspot["district"]
        }
        
        feats = extract_record_features(record)
        X.append(feats)
        
        prob = hotspot["base_prob"]
        if feats[4] == 1.0:  # Night
            prob += 0.15
        if loss > 200000:
            prob += 0.10
        prob = min(0.95, max(0.05, prob))
        
        label = 1 if random.random() < prob else 0
        y.append(label)
        
    return np.array(X), np.array(y)

def train_and_save():
    print("[INFO] Generating synthetic dataset...", flush=True)
    X, y = generate_synthetic_dataset(600)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("[INFO] Training Model 1: HistGradientBoostingClassifier...", flush=True)
    clf = HistGradientBoostingClassifier(max_iter=30, learning_rate=0.1, random_state=42)
    clf.fit(X_train, y_train)
    
    preds_proba = clf.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds_proba)
    f1 = f1_score(y_test, (preds_proba >= 0.5).astype(int))
    print(f"[RESULT] Model 1 ROC-AUC: {auc:.4f}, F1: {f1:.4f}", flush=True)
    
    clf_path = os.path.join(WEIGHTS_DIR, "hotspot_model.pkl")
    joblib.dump(clf, clf_path)
    print(f"[SAVED] {clf_path}", flush=True)
    
    print("[INFO] Training Model 3: IsolationForest...", flush=True)
    iso = IsolationForest(contamination=0.05, random_state=42, n_estimators=50)
    iso.fit(X_train)
    
    iso_path = os.path.join(WEIGHTS_DIR, "anomaly_model.pkl")
    joblib.dump(iso, iso_path)
    print(f"[SAVED] {iso_path}", flush=True)
    
    return {"roc_auc": auc, "f1": f1}

if __name__ == "__main__":
    train_and_save()
