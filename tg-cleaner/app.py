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
TELEGRAM_WEBHOOK_URL = f"{settings.WEBHOOK_URL}/{settings.WEBHOOK_PATH}"

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    logger.info("Root endpoint")
    return {"message": "Done"}


@app.on_event("startup")
async def on_startup():
    await register_webhook()
    dp.include_router(messages_bot_router)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@webhook_api_router.post("")
async def telegram_webhook(request: dict):
    update = types.Update(**request)
    await dp.feed_update(bot=bot, update=update)


async def register_webhook():
    await bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)
    logger.info(f"""Webhook registered {TELEGRAM_WEBHOOK_URL}""")
    webhook_info = await bot.get_webhook_info()
    logger.info(f"""Webhook info: {webhook_info}""")


@messages_bot_router.message()
async def delete_system_messages(message: types.Message):
    if message.text:
        return
    try:
        await bot(DeleteMessage(chat_id=message.chat, message_id=message.message_id))
    except:
        return
