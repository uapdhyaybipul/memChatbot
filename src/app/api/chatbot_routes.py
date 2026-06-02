from langchain_openrouter import ChatOpenRouter
from langchain_groq import ChatGroq
from fastapi import APIRouter, HTTPException, Depends
from src.core.security import create_access_token
from src.core.config import settings
from src.core.dependencies import get_current_user

router = APIRouter()

model_open_router = ChatOpenRouter(model=settings.CHAT_MODEL, api_key=settings.OPEN_ROUTER_API_KEY)
model_groq = ChatGroq(model=settings.CHAT_MODEL, api_key=settings.GROQ_API_KEY)
@router.post("/chat")
async def chat_with_model(message: str, current_user: dict = Depends(get_current_user)):
    try:
        response = model_groq.invoke(message)
        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example usage (remove or comment out in production)
# response = model.invoke("Hello, how are you?")
# print(response)