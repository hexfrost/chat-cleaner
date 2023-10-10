import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.methods import DeleteMessage

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from . import settings


app = FastAPI()
webhook_api_router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
messages_bot_router = Router()
TELEGRAM_WEBHOOK_URL = f"{settings.WEBHOOK_URL}/webhook"

logger = logging.getLogger(__name__)




@app.post("/webhook")
async def telegram_webhook(request: dict):
    update = types.Update(**request)
    await dp.feed_update(bot=bot, update=update)


async def register_webhook():
    await bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)
    logger.info(f"""Webhook registered {TELEGRAM_WEBHOOK_URL}""")
    webhook_info = await bot.get_webhook_info()
    logger.info(f"""Webhook info: {webhook_info}""")


def delete_messages_filter(message: types.Message):
    if message.new_chat_participant:
        return True
    if message.left_chat_participant:
        return True
    # if message.new_chat_title:
    #     return True
    # if message.new_chat_photo:
    #     return True
    # if message.new_chat_members:
    #     return True
    return False

@messages_bot_router.message()
async def delete_messages_handler(message: types.Message):
    log = f"""
    delete_system_messages: 
    
    CHAT: {message.chat}, 
    
    MESSAGE: {message}
    """
    logger.debug(log)
    if message.chat not in settings.CHATS_TO_CLEAN:
        return
    if delete_messages_filter(message):
        try:
            await bot(DeleteMessage(chat_id=message.chat, message_id=message.message_id))
        except:
            return


@app.get("/")
async def root():
    logger.info("Root endpoint")
    return {"message": "Done"}


@app.on_event("startup")
async def on_startup():
    logger.info("Starting up actions")
    await register_webhook()
    dp.include_router(messages_bot_router)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
