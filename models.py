from pydantic import BaseModel

class BrandRequest(BaseModel):
    industry: str
    keywords: str
    tone: str

class ContentRequest(BaseModel):
    description: str
    tone: str
    content_type: str

class SentimentRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str

class LogoRequest(BaseModel):
    brand_name: str
    industry: str
    keywords: str
    color: str = "gold"
    style: str = "Minimalist"
    composition: str = "Icon + Text"
