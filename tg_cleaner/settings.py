import os
import random
from string import ascii_letters, digits

from dotenv import load_dotenv

load_dotenv()

# Required
BOT_TOKEN=os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHATS_TO_CLEAN= [int(x) for x in os.getenv("CHATS_TO_CLEAN").split(" ")]

# Optional
RANDON_WEBHOOK_PATH = "".join(random.choices(list(ascii_letters + digits), k=32))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", RANDON_WEBHOOK_PATH)
