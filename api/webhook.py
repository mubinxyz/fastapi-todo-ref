# api/webhook.py
from fastapi import APIRouter, Request, HTTPException, Header
from telegram import Update
from telegram_bot.bot import application
from core.config import settings

router = APIRouter(tags=["Telegram"])

@router.post("/webhook")
async def process_webhook(
    request: Request, 
    x_telegram_bot_api_secret_token: str = Header(None, alias="X-Telegram-Bot-Api-Secret-Token")
):
    # 1. Security Check: Verify the request is actually from Telegram
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    # 2. Parse JSON into a Telegram Update object
    json_data = await request.json()
    update = Update.de_json(json_data, application.bot)
    
    # 3. Hand off to the bot engine
    await application.process_update(update)
    
    return "ok"