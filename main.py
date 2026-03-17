print("🔥 THIS MAIN.PY IS RUNNING 🔥")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from models import BrandRequest, ContentRequest, SentimentRequest, ChatRequest, LogoRequest, BaseModel
import ai_service
import os

app = FastAPI()

@app.get("/")
def read_root():
    frontend_path = os.path.join(os.path.dirname(__file__), "Frontend.html")
    return FileResponse(frontend_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate-brand")
def brand(req: BrandRequest):
    return {"brands": ai_service.generate_brand_names(req.model_dump())}

@app.post("/api/generate-content")
def content(req: ContentRequest):
    return {"content": ai_service.generate_content(req.model_dump())}

@app.post("/api/analyze-sentiment")
def sentiment(req: SentimentRequest):
    return ai_service.analyze_sentiment(req.text)

@app.post("/api/chat")
def chat(req: ChatRequest):
    return {"reply": ai_service.chatbot_reply(req.message)}

@app.post("/api/generate-logo")
def logo(req: LogoRequest):
    return {"image": ai_service.generate_logo_image(req.model_dump())}
@app.get("/test-all")
def test():
    return {"status": "all routes loaded"}

class AskRequest(BaseModel):
    prompt: str
    system: str = ""

@app.post("/api/ask")
def ask(req: AskRequest):
    full_prompt = req.prompt
    if req.system:
        full_prompt = f"[System: {req.system}]\n\n{req.prompt}"
    return {"result": ai_service.ask_ai(full_prompt)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
