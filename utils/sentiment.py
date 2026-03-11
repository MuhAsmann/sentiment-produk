
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

    # Lists to store samples
    neg_reviews_sample = []
    pos_reviews_sample = []
    
    # Frequency counters
    neg_word_freq = {}
    pos_word_freq = {}
    
    NEG_KEYWORDS_LIST = {
        "jelek", "buruk", "kecewa", "lambat", "lama", "palsu", "kw", "pecah", 
        "rusak", "mati", "mahal", "tidak", "kurang", "bohong", "penipu", "rugi", 
        "parah", "nyesel", "menyesal", "cacat", "error", "salah", "beda", "tipu",
        "kecewa", "mengecewakan", "longgar", "lepas", "copot", "patah", "lecet",
        "kotor", "bau", "bekas", "second", "tipis", "kasar", "panas", "berisik",
        "lemot", "hang", "crash", "bocor", "sobek", "bolong", "luntur", "tolol",
        "bego", "goblok", "anjing", "bangsat", "males", "nyesal", "nyesel", 
        "kapok", "parah", "hancur", "ancur", "kecewa", "zonk", "sampah"
    }
    
    POS_KEYWORDS_LIST = {
        "bagus", "baik", "mantap", "keren", "puas", "cepat", "original", "asli",
        "aman", "ramah", "recomended", "murah", "berfungsi", "oke", "ok",
        "joss", "berkualitas", "lengkap", "rapi", "packing", "mulus", "sesuai",
        "deskripsi", "original", "ori", "tepat", "kilat", "cakep", "top", "puas"
    }

    for idx, res_list in enumerate(all_results):
        if not res_list:
            continue
            
        top_prediction = res_list[0]
        label = str(top_prediction.get("label", "Neutral")).lower()
        stats[top_prediction.get("label", "Neutral")] = stats.get(top_prediction.get("label", "Neutral"), 0) + 1
        
        comment_text = str(comments[idx])
        words = comment_text.lower().split()
        cleaned_words = ["".join(filter(str.isalnum, w)) for w in words]
        
        # Collect negative info
        if label == "negative":
            if len(neg_reviews_sample) < 5:
                neg_reviews_sample.append(comment_text)
            for w in cleaned_words:
                if w in NEG_KEYWORDS_LIST:
                    neg_word_freq[w] = neg_word_freq.get(w, 0) + 1
                    
        # Collect positive info
        elif label == "positive":
            if len(pos_reviews_sample) < 5:
                pos_reviews_sample.append(comment_text)
            for w in cleaned_words:
                if w in POS_KEYWORDS_LIST:
                    pos_word_freq[w] = pos_word_freq.get(w, 0) + 1

    # Sort and get top keywords
    top_neg_words = [word for word, count in sorted(neg_word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]
    top_pos_words = [word for word, count in sorted(pos_word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]

    pos_count = stats.get("Positive", 0)
    neg_count = stats.get("Negative", 0)
    neu_count = stats.get("Neutral", 0)
    
    average_score = (pos_count - neg_count) / total_count if total_count > 0 else 0
    
    return {
        "average": round(average_score, 2),
        "positive_pct": round(pos_count / total_count * 100, 1) if total_count > 0 else 0,
        "negative_pct": round(neg_count / total_count * 100, 1) if total_count > 0 else 0,
        "neutral_pct": round(neu_count / total_count * 100, 1) if total_count > 0 else 0,
        "count": total_count,
        "raw_stats": stats,
        "negative_samples": neg_reviews_sample,
        "top_negative_keywords": top_neg_words,
        "top_positive_keywords": top_pos_words
    }
