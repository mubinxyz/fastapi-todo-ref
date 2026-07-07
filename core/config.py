# core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ... existing settings ...
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- TELEGRAM SETTINGS ---
    TELEGRAM_BOT_TOKEN: str = "8595170556:AAFukf1I0NTwQxqqcgetROS2BzC-C0x-N_Y"
    # We will use Ngrok to generate this URL in Step 6
    TELEGRAM_WEBHOOK_URL: str = "https://fastapi-todo-ref.fastapicloud.dev/webhook" 
    # A random string to verify requests actually come from Telegram
    TELEGRAM_WEBHOOK_SECRET: str = "super_secret_webhook_token_123"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()