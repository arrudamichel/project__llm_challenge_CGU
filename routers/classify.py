from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def classify_text(input_data: str):
    return {"classification": "positive", "probability": 0.8}
