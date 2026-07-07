# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from api import todos, users, webhook # <--- Import webhook
from telegram_bot.bot import application, register_handlers
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    Base.metadata.create_all(bind=engine)
    
    # Initialize Bot
    register_handlers()
    await application.initialize()
    
    # Tell Telegram to send updates to our webhook URL
    # We wrap in try/except so the app doesn't crash if you are offline/testing locally
    try:
        await application.bot.set_webhook(
            url=settings.TELEGRAM_WEBHOOK_URL,
            secret_token=settings.TELEGRAM_WEBHOOK_SECRET,
            allowed_updates=["message", "callback_query"]
        )
        print(f"✅ Webhook set to: {settings.TELEGRAM_WEBHOOK_URL}")
    except Exception as e:
        print(f"⚠️ Could not set webhook (are you online?): {e}")

    yield # App runs here
    
    # --- SHUTDOWN ---
    await application.shutdown()

app = FastAPI(title="Level-Up Todo API", lifespan=lifespan)

app.include_router(users.router)
app.include_router(todos.router)
app.include_router(webhook.router) # <--- Register Webhook Route

@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the State-of-the-Art Todo API!"}