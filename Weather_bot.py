import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from middleware.middleware import SessionMiddleware
from secret_info import TOKEN
from handlers.smth import router
from commands.bot_cmds_list import commands
from database.engine import create_db, session_maker

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)
dp.message.middleware(SessionMiddleware(session_pool=session_maker))


async def main():
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeAllPrivateChats(), language_code='ru')
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
