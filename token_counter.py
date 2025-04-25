from vertexai import generative_models
from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform
from pymongo import MongoClient

class TokenCounter:
    def __init__(self, project, location, mongo_uri, db_name, collection_name):
        aiplatform.init(project=project, location=location)
        self.model = GenerativeModel("gemini-2.0-flash-lite")
        self.collection = MongoClient(mongo_uri)[db_name][collection_name]

    def count_tokens(self):
        docs = list(self.collection.find({"transcript": {"$exists": True, "$ne": ""}}))
        print(f"Found {len(docs)} transcripts.")
        total = 0

        for doc in docs:
            try:
                response = self.model.count_tokens(doc["transcript"])
                total += response.total_tokens
            except Exception as e:
                print(f"Failed to count tokens for {doc.get('video_url', '')}: {e}")

        print(f"\n✅ Total token count across all transcripts: {total}")
