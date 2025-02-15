from aiogram.types import BotCommand

commands = [
    BotCommand(command='send_location', description='Надішліть свою локацію боту'),
    BotCommand(command='today', description='Прогноз на сьогодні'),
    BotCommand(command='tomorrow', description='Прогноз на завтра'),
    BotCommand(command='5days', description='Прогноз на 5 днів'),
]
