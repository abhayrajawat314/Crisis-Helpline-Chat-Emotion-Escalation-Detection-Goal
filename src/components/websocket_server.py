# src/components/websocket_server.py

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.components.data_loader import add_message_to_conversation, get_full_conversation, reset_conversation
from src.components.predict_chain import CrisisHelplinePredictor

app = FastAPI()
predictor = CrisisHelplinePredictor()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            speaker = data.get("speaker")
            text = data.get("text")

            # Add to conversation
            add_message_to_conversation(speaker, text)
            
            # Get full conversation
            full_conversation = get_full_conversation()

            # Predict risk
            prediction = predictor.predict(full_conversation)

            response = {
                "risk_level": prediction.risk_level if prediction else "Unknown",
                "events": prediction.events if prediction else [],
                "rationale": prediction.rationale if prediction else "Could not parse prediction"
            }

            # Send prediction back
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("WebSocket disconnected.")
