# telegram_bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from database import SessionLocal
import models
import schemas
from services import todo_crud
from core.security import get_password_hash

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register or greet the user."""
    chat_id = update.effective_chat.id
    
    with SessionLocal() as db:
        # 1. Check if user exists by Telegram ID
        user = db.query(models.User).filter(models.User.telegram_id == chat_id).first()
        
        if not user:
            # 2. Create new user automatically
            # We generate a dummy email/password since they login via Telegram
            user = models.User(
                email=f"tg_{chat_id}@bot.local",
                hashed_password=get_password_hash("telegram_default_pw"),
                role="user",
                telegram_id=chat_id
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            await update.message.reply_text(f"👋 Welcome! Account created. Your ID is {user.id}.")
        else:
            await update.message.reply_text(f"👋 Welcome back! You have {len(user.todos)} todos.")

async def add_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a todo. Usage: /add Buy milk"""
    chat_id = update.effective_chat.id
    
    if not context.args:
        await update.message.reply_text("❌ Usage: /add <title>")
        return
        
    title = " ".join(context.args)
    
    with SessionLocal() as db:
        user = db.query(models.User).filter(models.User.telegram_id == chat_id).first()
        if not user:
            await update.message.reply_text("Please run /start first.")
            return
            
        # Reuse our existing service layer!
        todo_schema = schemas.TodoCreate(title=title, description="Added via Telegram")
        new_todo = todo_crud.create_todo(db, todo_schema, owner_id=user.id)
        await update.message.reply_text(f"✅ Added: {new_todo.title}")

async def list_todos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all todos."""
    chat_id = update.effective_chat.id
    
    with SessionLocal() as db:
        user = db.query(models.User).filter(models.User.telegram_id == chat_id).first()
        if not user:
            await update.message.reply_text("Please run /start first.")
            return
            
        todos = todo_crud.get_todos(db, owner_id=user.id)
        if not todos:
            await update.message.reply_text("🎉 You have no todos!")
            return
            
        response = "📋 **Your Todos:**\n"
        for t in todos:
            status = "✅" if t.is_completed else "⏳"
            response += f"{status} {t.title}\n"
            
        await update.message.reply_text(response, parse_mode="Markdown")