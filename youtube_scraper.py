import subprocess
import json
import datetime
import requests
from pymongo import MongoClient

class YouTubeScraper:
    def __init__(self, channel_url, mongo_uri, db_name, collection_name, start_date, include_keywords, exclude_keywords):
        self.channel_url = channel_url
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]
        self.start_date = start_date
        self.include_keywords = include_keywords
        self.exclude_keywords = exclude_keywords

    def fetch_video_list(self):
        print("Fetching video list...")
        cmd = ["yt-dlp", self.channel_url, "--flat-playlist", "--dump-json"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        return [json.loads(line) for line in result.stdout.strip().split("\n")]

    def process_videos(self):
        videos = self.fetch_video_list()
        print(f"Found {len(videos)} videos.")
        n = 0

        for video in videos:
            video_id = video["id"]
            url = f"https://www.youtube.com/watch?v={video_id}"

            if not self._process_single_video(url):
                continue
            n += 1

        print(f"\n✅ Done! Processed {n} out of {len(videos)} videos.")

    def _process_single_video(self, url):
        cmd = [
            "yt-dlp", "-j", "--write-auto-sub", "--skip-download",
            "--sub-lang", "en", "--write-sub", url
        ]

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
            data = json.loads(result.stdout)

            title = data.get("title", "")
            upload_date = datetime.datetime.strptime(data.get("upload_date"), "%Y%m%d")

            if upload_date < self.start_date or \
               self.include_keywords.lower() not in title.lower() or \
               any(ex in title.upper() for ex in self.exclude_keywords):
                return False

            transcript = self._download_transcript(data)
            if not transcript:
                return False

            record = {
                "video_title": title,
                "channel_name": data.get("channel"),
                "channel_id": data.get("channel_id"),
                "upload_date": upload_date,
                "video_url": url,
                "transcript": transcript,
                "view_count": data.get("view_count"),
                "like_count": data.get("like_count"),
                "duration": data.get("duration"),
                "tags": data.get("tags", []),
            }

            self.collection.update_one({"video_url": url}, {"$set": record}, upsert=True)
            print(f"Saved: {title}")
            return True

        except Exception as e:
            print(f"Error processing {url}: {e}")
            return False

    def _download_transcript(self, data):
        subtitles = data.get("automatic_captions") or data.get("subtitles")
        if subtitles and "en" in subtitles:
            url = subtitles["en"][0]["url"]
            return requests.get(url).text
        return ""
