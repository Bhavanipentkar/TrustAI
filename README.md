# TrustAI – AI Trust Score Engine

TrustAI is a beginner-friendly hackathon project that evaluates the trustworthiness of text by extracting claims, verifying them with AI using Ollama, detecting hallucination risk, and generating a trust score.

## Project structure

- `backend/` – FastAPI backend with modular services for claim extraction, verification, hallucination detection, and scoring.
- `frontend/` – React frontend that sends text to the backend and displays results.

## How to run the backend

1. Start the Ollama server locally so the backend can use `llama3`:
   ```bash
   ollama daemon
   ```
2. Open a terminal in the `TrustAI/backend` folder.
3. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
5. The backend will run at `http://localhost:8000`.

## How to run the frontend

1. Open a terminal in the `TrustAI/frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend app:
   ```bash
   npm run dev
   ```
4. Open the URL shown by Vite, typically `http://localhost:5173`.

## Notes

- The backend uses mocked AI logic and rule-based heuristics so it can run without external AI APIs.
- Use the frontend textarea to paste text, then click "Analyze" to see the trust score, verdict, and hallucination risk.
