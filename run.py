
import os
import sys
from dotenv import load_dotenv

# Load explicitly here before any imports that use them
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("Sentiment Comparator App is running...")
    print("URL: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
