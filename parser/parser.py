import asyncio
import logging
import ast
from typing import Dict

import aiohttp
from secret_info import API_KEY
from database.redis_cache import Cache

LOCATION_URL = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
FORECAST_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/'

FORECAST_DAYS = {
    'today': 0,
    'tomorrow': 1,
}


class APIExpireException(BaseException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


async def make_async_session():
    return aiohttp.ClientSession()


async def get_location_key(location_data: str, session: aiohttp.ClientSession):
    params = {
        'apikey': API_KEY,
        'q': location_data,
    }
    response = await session.get(url=LOCATION_URL, params=params)
    return await response.json()


async def get_weather(location_key: str, session: aiohttp.ClientSession):
    params = {
        'apikey': API_KEY,
        'language': 'uk-ua'
    }
    finally_url = f'{FORECAST_URL}{5}day/{location_key}'
    response = await session.get(url=finally_url, params=params)
    return await response.json()


async def make_message(forecast_data: Dict):
    message = f'''Прогноз на {forecast_data['Date'][:10]}: \
    \nМін.{int((forecast_data['Temperature']['Minimum']['Value']-32)/1.8)} \
    Макс.{int((forecast_data['Temperature']['Maximum']['Value']-32)/1.8)}
    '''
    return message


async def make_prognoses(user_location: str):
    session = await make_async_session()
    try:
        location_key = await get_location_key(user_location, session)
        await asyncio.sleep(1)
        forecast = await get_weather(location_key['Key'], session)
    except KeyError:
        raise APIExpireException('Api access expire')
    finally:
        await session.close()
    return forecast


async def make_forecast(day: str, user_location: str, user_id: int):
    if result := await Cache.get(user_id):
        result = ast.literal_eval(result.decode('utf-8'))
    else:
        result = await make_prognoses(user_location)
        await Cache.set(user_id, data=str(result))
    if day in FORECAST_DAYS.keys():
        return await make_message(result['DailyForecasts'][FORECAST_DAYS.get(day)])
    str_forecast = ''
    for i in result['DailyForecasts']:
        str_forecast += await make_message(i)
    return str_forecast
