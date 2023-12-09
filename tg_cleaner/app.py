import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.methods import DeleteMessage
from aiogram.filters import Filter, or_f

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
    logger.debug(f"telegram_webhook: Got update: {update}")
    await dp.feed_update(bot=bot, update=update)


@app.get("/")
async def root():
    return {"status": "ok"}


async def register_webhook():
    await bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)
    logger.info(f"""Webhook registered {TELEGRAM_WEBHOOK_URL}""")
    webhook_info = await bot.get_webhook_info()
    logger.info(f"""Webhook info: {webhook_info}""")


class JoinUserFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if hasattr(message, "new_chat_participant"):
            if message.new_chat_participant:
                logger.debug(f"JoinUserFilter: filter passed for message: {message}")
                return True

class LeftUserFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if hasattr(message, "left_chat_participant"):
            if message.left_chat_participant:
                logger.debug(f"LeftUserFilter: filter passed for message: {message}")
                return True


class PinnedMessageFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if message.pinned_message:
            logger.debug(f"PinnedMessageFilter: filter passed for message: {message}")
            return True


TO_DELETE_FILTERS = (JoinUserFilter(), LeftUserFilter(), PinnedMessageFilter())


@messages_bot_router.message(or_f(*TO_DELETE_FILTERS))
async def delete_messages_handler(message: types.Message):
    try:
        await bot(DeleteMessage(
            chat_id=message.chat.id,
            message_id=message.message_id)
        )
    except Exception as e:
        logger.error(f"delete_messages_handler: Error deleting message: {e}")
    finally:
        logger.debug(f"delete_messages_handler: DELETED message {message}")


@app.on_event("startup")
async def on_startup():
    logger.info("Starting up actions")
    await register_webhook()
    dp.include_router(messages_bot_router)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
