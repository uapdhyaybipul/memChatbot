from fastapi import FastAPI
from src.app.api import routes_auth, chatbot_routes
from src.middleware.logging_middleware import LoggingMiddleware
from src.core.custom_exception import register_exception_handlers

app = FastAPI()

app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)
app.include_router(routes_auth.router,tags=["Authentication"])
app.include_router(chatbot_routes.router,tags=["Chatbot"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)