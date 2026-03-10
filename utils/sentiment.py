
# List of Indonesian sentiment words (simplified for demo)
# In production, use InSet Lexicon or a pre-trained model like IndoBERT

POSITIVE_WORDS = {
    "bagus", "baik", "mantap", "keren", "puas", "cepat", "original", "asli",
    "aman", "ramah", "recomended", "cepat", "murah", "berfungsi", "oke", "ok",
    "terima", "kasih", "thanks", "joss", "original", "berkualitas", "lengkap",
    "rapi", "packing", "respons", "kilat", "mulus", "sesuai", "deskripsi"
}

NEGATIVE_WORDS = {
    "jelek", "buruk", "kecewa", "lambat", "lama", "palsu", "kw", "pecah",
    "rusak", "mati", "mahal", "tidak", "kurang", "bohong", "penipu", "rugi",
    "parah", "nyesel", "menyesal", "cacat", "error", "salah", "beda", "tipu"
}

def analyze_sentiment(text):
    if not text or not isinstance(text, str):
        return 0, "neutral"
    
    text = text.lower()
    score = 0
    words = text.split()
    
    for word in words:
        if word in POSITIVE_WORDS:
            score += 1
        elif word in NEGATIVE_WORDS:
            score -= 1
            
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"
        
    return score, label

def get_sentiment_summary(comments):
    total_score = 0
    count = len(comments)
    if count == 0:
        return {"average": 0, "positive": 0, "negative": 0, "neutral": 0, "count": 0}
    
    stats = {"positive": 0, "negative": 0, "neutral": 0}
    
    for comment in comments:
        score, label = analyze_sentiment(comment)
        total_score += score
        stats[label] += 1
        
    return {
        "average": round(total_score / count, 2),
        "positive_pct": round(stats["positive"] / count * 100, 1),
        "negative_pct": round(stats["negative"] / count * 100, 1),
        "neutral_pct": round(stats["neutral"] / count * 100, 1),
        "count": count,
        "raw_stats": stats
    }
