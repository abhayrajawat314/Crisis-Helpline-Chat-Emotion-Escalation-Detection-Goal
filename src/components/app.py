from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from src.components.predict_chain import CrisisHelplinePredictor
from src.entity.config_entity import PredictionOutput
from src.components.data_loader import (
    add_message_to_conversation,
    get_full_conversation,
    reset_conversation
)

app = FastAPI()
predictor = CrisisHelplinePredictor(model_repo_id="HuggingFaceTB/SmolLM3-3B", temperature=0)


class MessageInput(BaseModel):
    speaker: str  
    text: str

@app.post("/predict")
def predict(message: MessageInput):
    
    add_message_to_conversation(message.speaker, message.text)

    full_conversation = get_full_conversation()

    result: Optional[PredictionOutput] = predictor.predict(full_conversation)

    if result:
        return {
            "risk_level": result.risk_level,
            "events": result.events,
            "rationale": result.rationale
        }
    else:
        return {"error": "Prediction failed."}


@app.post("/reset")
def reset():
    reset_conversation()
    return {"message": "Conversation has been reset."}
