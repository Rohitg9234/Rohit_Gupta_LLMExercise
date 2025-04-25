from youtube_scraper import YouTubeScraper
from llm_processor import LLMProcessor
from token_counter import TokenCounter
import datetime

# Common settings
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "youtube_data"

if __name__ == "__main__":
    # 1. Scrape YouTube
    scraper = YouTubeScraper(
        channel_url="https://www.youtube.com/@theteslaguy3247",
        mongo_uri=MONGO_URI,
        db_name=DB_NAME,
        collection_name="tsla_videos",
        start_date=datetime.datetime(2024, 1, 1),
        include_keywords="TSLA",
        exclude_keywords=["NVDA", "AMD", "AAPL", "META"]
    )
    scraper.process_videos()

    # 2. Process transcripts using Gemini
    processor = LLMProcessor(
        project="########",
        location="us-central1",
        mongo_uri=MONGO_URI,
        db_name=DB_NAME,
        input_collection="tsla_videos",
        output_collection="tsla_llm_transcripts"
    )
    processor.run()

    # 3. Count tokens
    counter = TokenCounter(
        project="########",
        location="us-central1",
        mongo_uri=MONGO_URI,
        db_name=DB_NAME,
        collection_name="tsla_videos"
    )
    counter.count_tokens()
