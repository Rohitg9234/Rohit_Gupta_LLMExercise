# LLM YouTube Analysis – TSLA Focus

## Overview
This project scrapes YouTube videos about TSLA, extracts transcripts, uses Google's Gemini model to analyze them, and stores structured JSON in MongoDB.

## Tech Stack
- Python
- Vertex AI (Gemini 2.0 Flash)
- MongoDB (local)
- yt-dlp
- Google Sheets (exported results)
- MongoDB Compass (GUI used in demo)


## Tech Stack
- Python
- Vertex AI (Gemini 2.0 Flash)
- MongoDB (local)
- yt-dlp
- Google Sheets (exported results)
- MongoDB Compass (GUI used in demo)

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/Rohitg9234/Rohit_Gupta_LLMExercise.git
cd Rohit_Gupta_LLMExercise
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Vertex AI
Ensure you have:
- Google Cloud SDK
- Enabled Vertex AI API
- Authenticated via `gcloud auth application-default login`

### 5. Run the scripts
```bash
python main.py
```

## MongoDB
- Database: `youtube_data`
- Collections:
  - `tsla_videos`
  - `tsla_llm_transcripts`

## Output Format
The Gemini model returns JSON like:
```json
{
  "narrative": "DECISIVE",
  "direction": "LONG",
  "Support": [176.0, 172.0],
  "Resistance": [185.0],
  "Buy_Area": [[176.0, 173.0]],
  "Sell_Area": [[185.0, 187.5]]
}
```

