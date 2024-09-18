from fastapi import APIRouter, Request, Depends
from datetime import timedelta

from app.database import main_func, get_all_currency, get_all_positions
from app.charts import get_currency_chart_with_impulse

from fastapi_cache.decorator import cache
import time

from fastapi.templating import Jinja2Templates

from cachetools import TTLCache

from starlette.responses import HTMLResponse



router = APIRouter(
    prefix='/screener',
    tags=['Фронтэнд']
)


templates = Jinja2Templates(directory='app/templates')





@router.get('/impulses', name='impulses')
async def get_impulses(
    request: Request, 
):
    for_templates=await main_func()

    print(for_templates)

    return templates.TemplateResponse(
        name='screener.html', 
        context={'request':request,
                'for_templates': for_templates,
                },
        )




@router.get("/positions", response_class=HTMLResponse, name='positions') 
async def read_positions(request: Request): 

    currency_list = await get_all_currency()
    positions = await get_all_positions()

    for position in positions:
        position.date_open = position.date_open.strftime('%Y-%m-%d %H:%M:%S')
        chart = await get_currency_chart_with_impulse(position.symbol,60, currency_list['Bybit']['Future'][position.symbol]['min_step'], position)
        position.chart = chart  # Добавляем новое поле со значением 5

    return templates.TemplateResponse(
        "positions.html", {"request": request, 'positions': positions}
        )




cache = TTLCache(maxsize=100, ttl=600) 

@router.get('/coin_info/{symbol}/{tf}', response_class=HTMLResponse) 
async def get_coin_info(request: Request, symbol: str, tf: str):

    tf = int(tf) 
    # Генерируем уникальный ключ для кэша 
    cache_key = f"{symbol}_{tf}" 

    

    if cache_key in cache:
        print('беру из кэша')
        html_content = cache[cache_key] 
    else: 
        currency_list = await get_all_currency()
        chart = await get_currency_chart_with_impulse(symbol,tf, currency_list['Bybit']['Future'][symbol]['min_step'])

        response = templates.TemplateResponse( 
            name='coin_info.html', 
            context={'request': request, 'chart' : chart, 'symbol' : symbol}, 
        ) 

        html_content = response.body.decode() 

        cache[cache_key] = html_content

    return HTMLResponse(content=html_content)