
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserLocation


class LocationState(StatesGroup):
    authorized_user = State()


async def my_set_state(state: FSMContext, user_location: str):
    await state.set_state(LocationState.authorized_user)
    await state.update_data(authorized_user=user_location)


async def add_user_location(message: types.Message, state: FSMContext, session: AsyncSession):
    location_data = f'{message.location.latitude},{message.location.longitude}'
    await my_set_state(state, location_data)
    obj = UserLocation(
        user_id=message.from_user.id,
        location=location_data,
    )

    session.add(obj)
    await session.commit()


async def update_user_location(message: types.Message, state: FSMContext, session: AsyncSession):
    location_data = f'{message.location.latitude},{message.location.longitude}'
    await my_set_state(state, location_data)
    query = update(UserLocation).where(UserLocation.user_id == message.from_user.id).values(
        location=location_data
    )
    await session.execute(query)
    await session.commit()


async def get_user_location(user_id: int, session: AsyncSession):
    query = select(UserLocation).where(UserLocation.user_id == user_id)
    result = await session.execute(query)
    if result:
        return result.scalar().location
    return None

