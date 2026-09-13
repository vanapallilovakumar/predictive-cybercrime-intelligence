import math
from datetime import datetime
from typing import Dict, Any, List, Tuple
import h3

def geo_to_h3_safe(lat: float, lng: float, resolution: int = 8) -> str:
    """Safely converts latitude and longitude to H3 hex index across h3-py versions."""
    try:
        if hasattr(h3, "latlng_to_cell"):
            return h3.latlng_to_cell(lat, lng, resolution)
        elif hasattr(h3, "geo_to_h3"):
            return h3.geo_to_h3(lat, lng, resolution)
    except Exception:
        pass
    return f"88{abs(hash((lat, lng, resolution))) % 10000000000000:013x}f"

def h3_to_geo_boundary_safe(h3_index: str) -> List[Tuple[float, float]]:
    """Returns boundary coordinates [(lat, lng), ...] for an H3 cell."""
    try:
        if hasattr(h3, "cell_to_boundary"):
            return list(h3.cell_to_boundary(h3_index))
        elif hasattr(h3, "h3_to_geo_boundary"):
            return list(h3.h3_to_geo_boundary(h3_index))
    except Exception:
        pass
    return []

TYPOLOGY_MAP = {
    "otp fraud": 0,
    "upi fraud": 1,
    "digital arrest": 2,
    "job fraud": 3,
    "investment scam": 4,
    "loan app extortion": 5,
    "other": 6
}

def extract_record_features(record: Dict[str, Any]) -> List[float]:
    """Extracts standardized numeric features for classifier and anomaly models."""
    loss = float(record.get("loss_amount_inr", 50000))
    log_loss = math.log1p(loss)
    
    # Parse timestamp
    ts_str = record.get("incident_timestamp", "")
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except Exception:
        dt = datetime.now()
        
    hour = dt.hour
    day = dt.weekday()
    is_night = 1.0 if (hour >= 22 or hour <= 5) else 0.0
    is_weekend = 1.0 if day in (5, 6) else 0.0
    
    typology_key = str(record.get("typology", "other")).lower()
    typ_code = float(TYPOLOGY_MAP.get(typology_key, 6))
    
    lat = float(record.get("latitude", record.get("center_lat", 24.0)))
    lon = float(record.get("longitude", record.get("center_lon", 86.0)))
    
    return [
        loss,
        log_loss,
        float(hour),
        float(day),
        is_night,
        is_weekend,
        typ_code,
        lat,
        lon
    ]
