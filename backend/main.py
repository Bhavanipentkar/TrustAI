from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router

app = FastAPI(
    title="TrustAI – AI Trust Score Engine",
    description="A simple FastAPI backend that evaluates the trustworthiness of text claims using Ollama.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)


@app.on_event("startup")
async def startup_event():
    print("Starting TrustAI backend with Ollama integration...")


@app.get("/")
async def root():
    return {
        "message": "TrustAI backend is running. Use POST /analyze to evaluate text with Ollama."
    }
