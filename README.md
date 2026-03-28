# ML API — Sentiment Analysis

A production-ready REST API for sentiment analysis, containerized with Docker.
Send text to the API, get back a sentiment label and confidence score.

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/predict` | Analyze one text |
| POST | `/predict/batch` | Analyze multiple texts |

## Example request
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely amazing"}'
```

## Example response
```json
{
  "text": "This product is absolutely amazing",
  "label": "POSITIVE",
  "confidence": 0.9999,
  "model": "distilbert-base-uncased-finetuned-sst-2-english"
}
```

---

## Run with Docker
```bash
docker pull danielmassoud/ml-api
docker run -p 8000:8000 ml-api
```

Then open http://localhost:8000/docs for the interactive API documentation.

## Run locally
```bash
git clone https://github.com/daniel-massoud/ml-api
cd ml-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Tech stack

- Python
- FastAPI -> REST API framework
- Docker -> containerization
- HuggingFace Transformers -> ML model
- DistilBERT -> sentiment classification model
- Uvicorn -> ASGI server
