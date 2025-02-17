import logging
from typing import Dict

import aiohttp
from secret_info import API_KEY

LOCATION_URL = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
FORECAST_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/'


async def make_async_session():
    return aiohttp.ClientSession()


async def get_location_key(location_data: str):
    session = await make_async_session()
    params = {
        'apikey': API_KEY,
        'q': location_data,
    }
    response = await session.get(url=LOCATION_URL, params=params)
    await session.close()
    return await response.json()


async def get_weather(location_key: str, num_of_days: int):
    session = await make_async_session()
    params = {
        'apikey': API_KEY,
        'language': 'uk-ua'
    }
    finally_url = f'{FORECAST_URL}{num_of_days}day/{location_key}'
    response = await session.get(url=finally_url, params=params)
    await session.close()
    return await response.json()


async def make_message(forecast_data: Dict):
    message = f'''Прогноз на {forecast_data['Date'][:10]}: \
    \nМін.{int((forecast_data['Temperature']['Minimum']['Value']-32)/1.8)} \
    Макс.{int((forecast_data['Temperature']['Maximum']['Value']-32)/1.8)}
    '''
    return message


async def make_prognoses(num_of_days: int, user_location: str):
    location_key = await get_location_key(user_location)
    forecast = await get_weather(location_key['Key'], num_of_days)
    return forecast


async def make_forecast(day: str, user_location: str):
    result = await make_prognoses(5, user_location)
    if day == 'today':
        return await make_message(result['DailyForecasts'][0])
    elif day == 'tomorrow':
        return await make_message(result['DailyForecasts'][1])
    str_forecast = ''
    for i in result['DailyForecasts']:
        str_forecast += await make_message(i)
    return str_forecast
