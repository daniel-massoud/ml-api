from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Create the FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="A production-ready API for sentiment analysis using DistilBERT",
    version="1.0.0"
)

# Load the model once when the server starts
# This is important — you never want to reload the model on every request
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

# Define what the incoming request must look like
class TextRequest(BaseModel):
    text: str

# Define what the response will look like
class PredictionResponse(BaseModel):
    text: str
    label: str
    confidence: float
    model: str

# Health check endpoint
# Companies always have this — it tells them the API is alive
@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "distilbert-sentiment"}

# Prediction endpoint
# This is the main one — send text, get sentiment back
@app.post("/predict", response_model=PredictionResponse)
def predict(request: TextRequest):
    result = sentiment_model(request.text)[0]
    
    return PredictionResponse(
        text=request.text,
        label=result["label"],
        confidence=round(result["score"], 4),
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

# Batch prediction endpoint
# Process multiple texts in one request — much more efficient
@app.post("/predict/batch")
def predict_batch(requests: list[TextRequest]):
    texts = [r.text for r in requests]
    results = sentiment_model(texts)
    
    return [
        {
            "text": texts[i],
            "label": results[i]["label"],
            "confidence": round(results[i]["score"], 4)
        }
        for i in range(len(texts))
    ]