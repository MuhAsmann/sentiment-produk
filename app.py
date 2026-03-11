
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load env variables at the top
load_dotenv()

from utils.scraper import scrape_product
from utils.sentiment import get_sentiment_summary
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    url1 = data.get('url1')
    url2 = data.get('url2')
    
    if not url1 or not url2:
        return jsonify({"error": "Dua URL produk diperlukan"}), 400
    
    p1 = scrape_product(url1)
    p2 = scrape_product(url2)
    
    if not p1 or not p2:
        return jsonify({"error": "Gagal mengambil data produk"}), 500
    
    # Analyze sentiment
    p1['sentiment'] = get_sentiment_summary(p1['reviews'])
    p2['sentiment'] = get_sentiment_summary(p2['reviews'])
    
    return jsonify({
        "product1": p1,
        "product2": p2,
        "comparison": {
            "winner": "Produk 1" if p1['sentiment']['average'] > p2['sentiment']['average'] else "Produk 2",
            "score_diff": round(abs(p1['sentiment']['average'] - p2['sentiment']['average']), 2)
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
