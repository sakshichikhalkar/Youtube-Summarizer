# YouTube Summarizer

A Chrome Extension + FastAPI backend that summarizes any YouTube video using AI. Paste a YouTube URL, get a clean bullet-point summary in seconds — without watching the entire video.


## What It Does

- Extracts transcripts from any YouTube video automatically
- Generates AI-powered summaries using Groq's LLaMA 3.3 70B model
- Lets you choose summary length — short, medium, or detailed
- Caches results in PostgreSQL so the same video is never processed twice
- Works directly from your browser via a Chrome Extension


## Tech Stack

**Backend**
- FastAPI — REST API framework
- PostgreSQL — database for storing and caching summaries
- SQLAlchemy — ORM for database operations
- Groq API (LLaMA 3.3 70B) — AI model for summarization
- youtube-transcript-api — transcript extraction
- slowapi — rate limiting (5 requests/minute)
- python-dotenv — environment variable management

**Frontend**
- Chrome Extension (Manifest V3)
- HTML, CSS, JavaScript

**Deployment**
- Railway (backend + PostgreSQL)



## Project Structure
Youtube-Summarizer/
├── main.py                  # FastAPI app entry point
├── database.py              # Database connection and session setup
├── models.py                # SQLAlchemy table definitions
├── requirements.txt
├── render.yaml              # Deployment configuration
├── routes/
│   └── summarize.py         # API endpoints
├── services/
│   ├── transcript.py        # YouTube transcript extraction
│   └── summarizer.py        # Groq AI summarization logic
└── chrome-extension/
├── manifest.json        # Chrome Extension configuration
├── popup.html           # Extension popup UI
├── popup.js             # Extension logic
└── popup.css            # Extension styling



## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/summarize` | Generate AI summary for a YouTube URL |
| GET | `/history` | View last 10 summaries (supports ?limit=N) |
| DELETE | `/summary/{id}` | Delete a specific summary by ID |
| GET | `/health` | Health check |



## How It Works
User clicks Summarize in Chrome Extension
↓
Extension sends YouTube URL to FastAPI backend
↓
Backend checks PostgreSQL cache first
↓
If cached → returns instantly (no AI call)
If not cached → extracts transcript via youtube-transcript-api
↓
Transcript sent to Groq AI with summarization prompt
↓
Summary returned, saved to PostgreSQL for future requests
↓
Result displayed in Chrome Extension popup



## Features

- **Smart caching** — same video + same summary type never calls AI twice
- **3 summary modes** — short (3 bullets), medium (5 bullets), detailed (paragraph)
- **Rate limiting** — 5 requests per minute per IP to prevent abuse
- **Full error handling** — handles disabled transcripts, invalid URLs, server downtime, non-YouTube pages
- **CORS enabled** — Chrome Extension can communicate with the backend securely



## Running Locally

**Prerequisites:** Python 3.11+, PostgreSQL, Chrome browser

**1. Clone the repository**
```bash
git clone https://github.com/sakshichikhalkar/Youtube-Summarizer.git
cd Youtube-Summarizer
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/youtube_summarizer_db

Get your free Groq API key at: https://console.groq.com

**5. Create PostgreSQL database**

Open pgAdmin and create a database called `youtube_summarizer_db`. Tables are created automatically when the server starts.

**6. Run the backend**
```bash
uvicorn main:app --reload
```

API runs at `http://localhost:8000`
Swagger UI at `http://localhost:8000/docs`

**7. Load Chrome Extension**

- Open Chrome and go to `chrome://extensions`
- Enable Developer Mode (top right toggle)
- Click "Load unpacked"
- Select the `chrome-extension/` folder



## Using The Extension

1. Open any YouTube video in Chrome
2. Click the YouTube Summarizer icon in your browser toolbar
3. Choose summary length from the dropdown (Short / Medium / Detailed)
4. Click "Summarize"
5. Read the AI-generated summary directly in the popup



## Deployment Note

Backend is deployed on Railway. Due to YouTube's IP restrictions on cloud server IPs, transcript fetching currently works via local setup. Proxy configuration (Webshare residential proxies) is the planned fix for full cloud deployment.



## What I Learned Building This

- Designing and structuring a production-level REST API with FastAPI
- PostgreSQL integration with SQLAlchemy ORM including caching patterns
- Integrating third-party AI APIs (Groq/LLaMA) into a backend pipeline
- Building a Chrome Extension from scratch and connecting it to a backend
- Debugging CORS issues between a browser extension and a local API
- Deploying a Python backend with a managed PostgreSQL database on Railway
- Error handling across all failure modes — invalid URLs, disabled transcripts, rate limits, server downtime



## Author

**Sakshi Chikhalkar**
BCA Final Year | Python Backend Developer
GitHub: https://github.com/sakshichikhalkar