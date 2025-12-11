from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import asyncio
from .session_manager import AISessionManager
from .webrtc_handler import WebRTCHandler

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

session_manager = AISessionManager()
webrtc_handler = WebRTCHandler()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "start_session":
                response = await session_manager.start_session(
                    message["title"], 
                    message["description"]
                )
                await websocket.send_text(json.dumps({
                    "type": "ai_response",
                    "content": response,
                    "speak": True
                }))
            
            elif message["type"] == "user_message":
                response = await session_manager.process_user_input(message["content"])
                await websocket.send_text(json.dumps({
                    "type": "ai_response",
                    "content": response,
                    "speak": True
                }))
            
            elif message["type"] == "voice_message":
                response = await session_manager.process_user_input(message["content"])
                await websocket.send_text(json.dumps({
                    "type": "ai_response",
                    "content": response,
                    "speak": True
                }))
            
            elif message["type"] == "webrtc_offer":
                answer = await webrtc_handler.handle_offer(message["sdp"])
                await websocket.send_text(json.dumps({
                    "type": "webrtc_answer",
                    "sdp": answer
                }))
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    # Remove the finally block that was causing double close

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)