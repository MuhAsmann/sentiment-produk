
import requests
import time
import os
from dotenv import load_dotenv

# Ensure .env variables are loaded
load_dotenv()

# Hugging Face API settings
HF_API_URL = os.getenv("HF_API_URL")
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_API_URL or not HF_TOKEN:
    raise ValueError("HF_API_URL and HF_TOKEN must be set in environment variables")

def call_hf_api(inputs):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": inputs}
    
    # Simple retry logic for 503 errors (model loading)
    for _ in range(5):
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                # Model is loading
                print(f"Model is loading, waiting 10 seconds...")
                time.sleep(10)
                continue
            else:
                print(f"HF API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error calling HF API: {e}")
            return None
    return None

def get_sentiment_summary(comments):
    if not comments:
        return {"average": 0, "positive_pct": 0, "negative_pct": 0, "neutral_pct": 0, "count": 0, "raw_stats": {}}

    stats = {"Positive": 0, "Negative": 0, "Neutral": 0}
    total_count = len(comments)
    
    # Process in batches of 50 to avoid API limits
    batch_size = 50
    all_results = []
    
    for i in range(0, total_count, batch_size):
        batch = comments[i : i + batch_size]
        # Ensure we're sending strings
        batch = [str(c) for c in batch if c]
        if not batch:
            continue
        results = call_hf_api(batch)
        
        if results:
            # results is a list of lists of dicts: [[{"label": "...", "score": ...}, ...], ...]
            all_results.extend(results)
        else:
            # Add placeholders for failed batch
            all_results.extend([[{"label": "Neutral", "score": 0.0}]] * len(batch))

    for res_list in all_results:
        if not res_list:
            continue
        # The first item is usually the top prediction
        top_prediction = res_list[0]
        label = top_prediction.get("label", "Neutral")
        stats[label] = stats.get(label, 0) + 1

    # Re-map to lowercase labels for compatibility with frontend if needed, 
    # but the model returns "Positive", "Negative", "Neutral"
    
    pos_count = stats.get("Positive", 0)
    neg_count = stats.get("Negative", 0)
    neu_count = stats.get("Neutral", 0)
    
    # Calculate a simple average score: Positive=1, Neutral=0, Negative=-1
    average_score = (pos_count - neg_count) / total_count if total_count > 0 else 0
    
    return {
        "average": round(average_score, 2),
        "positive_pct": round(pos_count / total_count * 100, 1) if total_count > 0 else 0,
        "negative_pct": round(neg_count / total_count * 100, 1) if total_count > 0 else 0,
        "neutral_pct": round(neu_count / total_count * 100, 1) if total_count > 0 else 0,
        "count": total_count,
        "raw_stats": stats
    }
