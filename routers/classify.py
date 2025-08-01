from services import sent_classifier
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel, model_validator
from typing import Optional

router = APIRouter()

# Lista de modelos suportados
SUPPORTED_MODELS = ["openai", "llama3.1"]

class SentimentRequest(BaseModel):
    input_data: str = Form(..., description="Texto para classificar o sentimento")
    model: str = Form(..., description="Modelo a ser usado")
    openai_api_key: Optional[str] = Form(None, description="Chave da API da OpenAI")

    @model_validator(mode="after")
    def validate_api_key(self) -> "SentimentRequest":
        if self.model == "openai" and not self.openai_api_key:
            raise ValueError("A chave da API da OpenAI é obrigatória ao usar o modelo 'openai'.")
        return self

@router.post("/")
def classify_text(request: SentimentRequest):
    if request.model == "openai":
        return sent_classifier.classify_sentiment_openai(request.input_data, api_key=request.openai_api_key)
    elif request.model == "llama3.1":
        return sent_classifier.classify_sentiment_llama(request.input_data)
    else:
        raise HTTPException(status_code=400, detail="Modelo não suportado.")
