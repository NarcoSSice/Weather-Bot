from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import my_set_state, add_user_location, update_user_location, get_user_location
from keyboard import key_buttons
from parser.parser import make_forecast

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    user_location = await get_user_location(message.from_user.id, session)
    await my_set_state(state, user_location)

    if user_location:
        await message.answer(text='Бачу ви вже тут не в перше. Бажаєте змінити локацію, чи одразу отримати прогноз?',
                             reply_markup=key_buttons.change_location_keyboard.as_markup(
                                 resize_keyboard=True
                             ))
    else:
        await message.answer(text='Для надання прогнозу погоди, мені потрібна твоя локація',
                             reply_markup=key_buttons.start_keyboard.as_markup(
                                 resize_keyboard=True
                             ))


@router.message(or_f(Command('send_location'), F.text.lower() == 'надіслати локацію',
                F.text.lower() == 'змінити локацію'))
async def send_location(message: types.Message):
    await message.answer(text='Для надання своєї локації натисни кнопку "надіслати локацію"',
                         reply_markup=key_buttons.start_keyboard.as_markup(
                             resize_keyboard=True
                         ))


@router.message(F.location)
async def add_location(message: types.Message, state: FSMContext, session: AsyncSession):
    user_location = await state.get_data()
    if user_location:
        await update_user_location(message, state, session)
        await message.answer(text='Вашу локацію змінено, який прогноз вам потрібен?',
                             reply_markup=key_buttons.authenticate_keyboard.as_markup(
                                 resize_keyboard=True
                             ))
    else:
        await message.answer(text='Я отримав вашу локацію, який прогноз вам потрібен?',
                             reply_markup=key_buttons.authenticate_keyboard.as_markup(
                                 resize_keyboard=True
                             ))
        await add_user_location(message, state, session)


@router.message(F.text.lower() == 'отримати прогноз')
async def give_forecast(message: types.Message):
    await message.answer(text='Який прогноз вам потрібен?',
                         reply_markup=key_buttons.authenticate_keyboard.as_markup(
                             resize_keyboard=True
                         ))


@router.message(or_f(Command('today'), F.text.lower() == 'прогноз на сьогодні'))
async def today_forecast(message: types.Message, state: FSMContext):
    user_loc = await state.get_data()
    forecast = await make_forecast('today', user_loc.get('authorized_user'))
    await message.answer(text=forecast)


@router.message(or_f(Command('tomorrow'), F.text.lower() == 'прогноз на завтра'))
async def tomorrow_forecast(message: types.Message, state: FSMContext):
    user_loc = await state.get_data()
    forecast = await make_forecast('tomorrow', user_loc.get('authorized_user'))
    await message.answer(text=forecast)


@router.message(or_f(Command('5days'), F.text.lower() == 'прогноз на 5 днів'))
async def five_days_forecast(message: types.Message, state: FSMContext):
    user_loc = await state.get_data()
    forecast = await make_forecast('5days', user_loc.get('authorized_user'))
    await message.answer(text=forecast)


@router.edited_message()
async def edited_echo(message: types.Message):
    await message.reply('Че редактируешь лох?')
