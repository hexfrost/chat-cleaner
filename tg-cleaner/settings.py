import os
import random
from string import ascii_letters, digits

from dotenv import load_dotenv

load_dotenv()

# Required
BOT_TOKEN=os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Optional
RANDON_WEBHOOK_PATH = "webhook:" + "".join(random.choices(list(ascii_letters + digits), k=32))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", RANDON_WEBHOOK_PATH)
