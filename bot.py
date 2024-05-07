import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


class Bot(Client):
    async def send_tip_info(self, chat_id, photo, title, addr, description='Send only CRYPT to this address'):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton('Back', callback_data='back')],
            ]
        )
        description.replace('CRYPT', title)
        caption = f'**{title}**\n'\
            f'{description}\n'\
            f'```{addr}```'
        await self.send_photo(chat_id, photo, caption, reply_markup=keyboard)
        print('tip info')

    


load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

if not os.path.exists("sessions"):
    os.mkdir("sessions")

bot = Bot(
    os.path.join("sessions", "u2berbot"),
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('USDT TRC20', callback_data='USDT TRC20')],
        [InlineKeyboardButton('USDT TON', callback_data='USDT TON')],
        [InlineKeyboardButton('Toncoin (TON)', callback_data='TON')],
        [InlineKeyboardButton('Bitcoin (BTC)', callback_data='BTC')],
        [InlineKeyboardButton('Cancel', callback_data='cancel')],
    ]
)

clicks = 2

@bot.on_message(filters.command(['start', 'help']))
async def start(bot: Bot, message):
    await bot.send_message(message.chat.id,
                    'Hey, I\'m U2BErBot! I can help you to download videos from YouTube.\n'\
                    'I am able to extract both video and audio tracks from the video.\n\n'\
                    'You can use me by sending a YouTube link to me.'
                    )


@bot.on_message(filters.command('tip'))
async def tip(bot: Bot, message):
    await bot.send_message(
        message.chat.id,
        'Choose a tipping currency:',
        reply_markup=keyboard
    )

@bot.on_callback_query()
async def callback_query(bot: Bot, query: CallbackQuery):
    global clicks
    clicks += 1
    
    data = query.data
    
    match data:
        case 'USDT TRC20':
            await bot.delete_messages(query.message.chat.id, query.message.id)
            await bot.send_tip_info(query.message.chat.id, 'https://i.stack.imgur.com/Z1NRq.png', query.data, 'TAVxjUzxYge5Ax2sA6bJHQHC1zw7uP3Je2')
        case 'USDT TON':
            pass
        case 'TON':
            pass
        case 'BTC':
            pass
        case 'back':
            await bot.delete_messages(query.message.chat.id, query.message.id)
            await bot.send_message(query.message.chat.id, 'Choose a tipping currency:', reply_markup=keyboard)
        case 'cancel':
            message_id = query.message.id
            for _ in range(clicks):
                await bot.delete_messages(query.message.chat.id, message_id)
                message_id -= 1
        case _:
            pass


if __name__ == "__main__":
    bot.run()
