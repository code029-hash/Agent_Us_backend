import newspaper
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Download necessary NLTK components
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def clean_text(text):
    """Clean and preprocess input text."""
    if not text or not isinstance(text, str):
        return ""

    words = text.split()
    return ' '.join([word for word in words if len(word) < 100 and word.isalpha()])

def summarize_text(text):
    """Generate a coherent summary in 30-40 words."""
    try:
        cleaned = clean_text(text)
        words = cleaned.split()

        if len(words) < 40:
            return cleaned  # Return short text as-is

        sentences = sent_tokenize(cleaned)
        if len(sentences) < 3:
            return ' '.join(words[:40])  # Fallback to first 40 words

        # Extract important words
        stop_words = set(stopwords.words('english'))
        keywords = [word.lower() for word in words if word.lower() not in stop_words and len(word) > 2]

        word_freq = nltk.FreqDist(keywords)
        max_freq = max(word_freq.values(), default=1)  # Prevent division by zero

        # Score sentences
        sentence_scores = {}
        for i, sent in enumerate(sentences):
            sent_words = [word.lower() for word in word_tokenize(sent)]
            score = sum(word_freq[word] / max_freq for word in sent_words if word in word_freq)
            sentence_scores[i] = score / len(sent_words)  # Normalize score

        # Select top-ranked sentences
        sorted_sents = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary = []
        word_count = 0

        for idx, _ in sorted_sents:
            sent_words = sentences[idx].split()
            if word_count + len(sent_words) <= 40:
                summary.append(sentences[idx])
                word_count += len(sent_words)
                if word_count >= 30:
                    break

        if 30 <= word_count <= 40:
            return ' '.join(summary)

        # Fallback: First 40 words maintaining sentence integrity
        fallback = []
        current_words = 0
        for sent in sentences:
            sent_words = sent.split()
            if current_words + len(sent_words) <= 40:
                fallback.append(sent)
                current_words += len(sent_words)
            else:
                remaining = 40 - current_words
                if remaining > 3:
                    fallback.append(' '.join(sent_words[:remaining]))
                break

        return ' '.join(fallback)

    except Exception as e:
        logging.error(f"Summarization error: {str(e)}")
        return ' '.join(cleaned.split()[:40])  # Final fallback

def fetch_article(url):
    """Fetch article content with error handling."""
    try:
        article = newspaper.Article(
            url, language='en', fetch_images=False, request_timeout=10, memoize_articles=False
        )

        article.download()
        article.parse()

        return (
            article.title or "Untitled Article",
            ', '.join(article.authors) if article.authors else "Unknown Author",
            article.publish_date.strftime("%Y-%m-%d") if article.publish_date else "Unknown Date",
            urlparse(url).netloc.replace('www.', '').title(),
            article.text or ""
        )
    except Exception as e:
        logging.error(f"Article fetch error for {url}: {str(e)}")
        return "Error", "Error", "Error", "Error", ""

def summarize_article(url):
    """Summarize an article given its URL."""
    try:
        title, authors, date, publisher, text = fetch_article(url)
        if not text.strip():
            return title, publisher, date, "No content available"

        summary = summarize_text(text)
        return title, publisher, date, summary
    except Exception as e:
        logging.error(f"Article processing failed: {str(e)}")
        return "Error", "Error", "Error", "Summary unavailable"
