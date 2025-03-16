from flask import Flask, jsonify, request
from summarizer import summarize_article
from tone_changer import change_tone
from flask_cors import CORS
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Global cache for storing fetched news
cached_news = []

# News API Key
API_KEY = "ff6140b6401d478e9efba563553b4f8a"

def fetch_news():
    """Fetch news articles from API"""
    url = f"https://newsapi.org/v2/everything?q=Donald+Trump&apiKey={API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])

    news_urls = [item["url"] for item in articles[:15] if "url" in item]
    return news_urls

def load_news():
    """Fetch and store summarized news"""
    global cached_news
    try:
        urls = fetch_news()
        cached_news = []

        for url in urls:
            try:
                title, publisher, date, summary = summarize_article(url)
                if summary and summary != "No content available":
                    cached_news.append({
                        "title": title,
                        "neutral_summary": summary,
                        "url": url,
                        "publisher": publisher,
                        "publish_date": date
                    })
                else:
                    logging.warning(f"Skipped invalid article: {url}")

            except Exception as e:
                logging.error(f"Failed to process {url}: {str(e)}")

        logging.info(f"Loaded {len(cached_news)} valid articles")

    except Exception as e:
        logging.error(f"News loading failed: {str(e)}")
        cached_news = []

# Load news once when the app starts
with app.app_context():
    load_news()

@app.route("/news", methods=["GET"])
@app.route("/news", methods=["GET"])
def get_news():
    """Fetch summarized news with optional tone adjustment"""
    try:
        tone = request.args.get("tone", "neutral")

        if not cached_news:
            load_news()

        processed_news = []

        if tone == "neutral":
            # Return neutral summary but rename the key to "summary"
            for item in cached_news:
                processed_news.append({
                    "title": item["title"],
                    "summary": item["neutral_summary"],  # Use neutral_summary but rename it to summary
                    "url": item["url"],
                    "publisher": item["publisher"],
                    "publish_date": item["publish_date"]
                })
        else:
            # Modify summaries based on the requested tone
            summaries = [item["neutral_summary"] for item in cached_news]
            modified_summaries = change_tone(summaries, tone)

            for idx, item in enumerate(cached_news):
                processed_news.append({
                    "title": item["title"],
                    "summary": modified_summaries[idx],  # Use the modified summary
                    "url": item["url"],
                    "publisher": item["publisher"],
                    "publish_date": item["publish_date"]
                })

        return jsonify({"news": processed_news})

    except Exception as e:
        logging.error(f"Error fetching news: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
