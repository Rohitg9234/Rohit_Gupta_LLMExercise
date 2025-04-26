import argparse
import datetime
from youtube_scraper import YouTubeScraper
from llm_processor import LLMProcessor
from token_counter import TokenCounter

# Common settings
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "youtube_data"

def main():
    parser = argparse.ArgumentParser(description="YouTube Scraper and Processor")

    # Arguments we can pass via command line
    parser.add_argument("--channel_url", type=str, required=True, help="YouTube channel URL")
    parser.add_argument("--stock_name", type=str, required=True, help="Stock name to include in filtering (e.g., TSLA)")
    parser.add_argument("--start_date", type=str, default="2024-01-01", help="Start date for scraping in YYYY-MM-DD format")
    parser.add_argument("--include_keywords", type=str, nargs='+', help="Keywords to include (default is stock_name)", default=None)
    parser.add_argument("--exclude_keywords", type=str, nargs='+', help="Keywords to exclude", default=["NVDA", "AMD", "AAPL", "META"])

    args = parser.parse_args()

    # If include_keywords is not passed, use [stock_name]
    include_keywords = args.include_keywords if args.include_keywords else [args.stock_name]

    # 1. Scrape YouTube
    scraper = YouTubeScraper(
        channel_url=args.channel_url,
        mongo_uri=MONGO_URI,
        db_name=DB_NAME,
        collection_name="tsla_videos",
        start_date=datetime.datetime.strptime(args.start_date, "%Y-%m-%d"),
        include_keywords=include_keywords,
        exclude_keywords=args.exclude_keywords
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

if __name__ == "__main__":
    main()
