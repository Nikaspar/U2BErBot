import os
from dotenv import load_dotenv
from pyrogram import Client


load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

os.mkdir("sessions", exist_ok=True)

bot = Client(
    os.path.join("sessions", "u2berbot"),
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash
)

# TODO: Add your code here

if __name__ == "__main__":
    bot.run()
