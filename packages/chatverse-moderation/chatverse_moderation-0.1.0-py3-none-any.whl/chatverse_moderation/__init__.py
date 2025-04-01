import re
import datetime
import logging
import html
from textblob import TextBlob

class ChatUtils:
    """Utility class for chat message processing, including sanitization, profanity filtering, sentiment analysis, and logging."""

    def __init__(self):
        self.bad_words = ["badword", "inappropriate", "fuck"]  # Expand this list
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="chat.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def sanitize_message(self, message: str) -> str:
        """Sanitizes the message input to prevent XSS and other injection attacks."""
        original_message = message

        # Remove JavaScript event handlers (e.g., onclick, onerror)
        message = re.sub(r'on\w+\s*=\s*"[^"]+"', '', message, flags=re.IGNORECASE)
        message = re.sub(r'on\w+\s*=\s*\'[^\']+\'', '', message, flags=re.IGNORECASE)

        # Remove harmful script, iframe, or object tags
        message = re.sub(r"<(script|iframe|object|embed)[^>]*>.*?</\1>", "", message, flags=re.IGNORECASE | re.DOTALL)

        # Escape remaining HTML tags safely
        sanitized_message = html.escape(message)

        # Log sanitization if changes were made
        if original_message != sanitized_message:
            self.logger.warning(f"🚨 Message sanitized: {original_message} -> {sanitized_message}")

        return sanitized_message

    def filter_profanity(self, message: str) -> str:
        """Replaces offensive words with asterisks while keeping some letters visible."""
        for word in self.bad_words:
            censored_word = word[0] + '*' * (len(word) - 2) + word[-1]  # Example: "badword" -> "b*****d"
            message = re.sub(rf"\b{word}\b", censored_word, message, flags=re.IGNORECASE)
        return message

    def analyze_sentiment(self, message: str) -> tuple:
        """Performs sentiment analysis and returns both the sentiment category and emoji."""
        sentiment_score = TextBlob(message).sentiment.polarity

        if sentiment_score > 0.5:
            return "very positive 😍", sentiment_score
        elif 0.2 < sentiment_score <= 0.5:
            return "positive 😊", sentiment_score
        elif -0.2 <= sentiment_score <= 0.2:
            return "neutral 😐", sentiment_score
        elif -0.5 <= sentiment_score < -0.2:
            return "negative 😡", sentiment_score
        else:
            return "very negative 🤬", sentiment_score

    def format_timestamp(self) -> str:
        """Returns a formatted timestamp for messages."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_message(self, sender: str, message: str, sentiment: str, sentiment_score: float):
        """Logs chat messages with sentiment analysis and score."""
        log_entry = f"{self.format_timestamp()} - {sender}: {message} | Sentiment: {sentiment} (Score: {sentiment_score:.2f})"
        self.logger.info(log_entry)
