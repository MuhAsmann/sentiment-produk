
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("Sentiment Comparator App is running...")
    print("URL: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
