from vertexai import generative_models
from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform
from pymongo import MongoClient
import datetime

class LLMProcessor:
    def __init__(self, project, location, mongo_uri, db_name, input_collection, output_collection):
        aiplatform.init(project=project, location=location)
        self.model = GenerativeModel("gemini-2.0-flash-lite")
        db = MongoClient(mongo_uri)[db_name]
        self.input_collection = db[input_collection]
        self.output_collection = db[output_collection]

    def run(self, start_date=datetime.datetime(2024, 1, 1)):
        docs = list(self.input_collection.find({"upload_date": {"$gte": start_date}})
                    .sort("upload_date", -1).limit(120))

        for doc in docs:
            self._process_document(doc)

    def _process_document(self, doc):
        transcript = doc.get("transcript", "")
        if not transcript:
            return

        prompt = self._build_prompt(transcript)

        try:
            response = self.model.generate_content(prompt, generation_config={"temperature": 0.2, "max_output_tokens": 1024})
            structured_json = response.text

            record = {
                "video_id": doc.get("video_url", "").split("v=")[-1],
                "channel_id": doc.get("channel_id"),
                "channel_name": doc.get("channel_name"),
                "upload_date": doc.get("upload_date"),
                "video_title": doc.get("video_title"),
                "video_url": doc.get("video_url"),
                "llm_response": structured_json
            }

            self.output_collection.update_one({"video_id": record["video_id"]}, {"$set": record}, upsert=True)
            print(f"Processed: {doc['video_title']}")

        except Exception as e:
            print(f"Error processing video: {e}")

    def _build_prompt(self, transcript):
        return f"""
        Analyze the following financial transcript. 
        Return JSON in this format:
        {{
          "narrative": "DECISIVE" or "NON-DECISIVE",
          "direction": "LONG" or "SHORT",
          "Support": [<floats>],
          "Resistance": [<floats>],
          "Buy_Area": [<tuples with descending float ranges>],
          "Sell_Area": [<tuples with ascending float ranges>]
        }}
        Transcript:
        \"\"\"
        {transcript}
        \"\"\"
        """
