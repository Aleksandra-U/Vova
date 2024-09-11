from fastapi import APIRouter, Request, Depends

from app.database import get_symbol_tf_impulses, get_uniq_coin, get_sort_by_ft,amount_coin_in_levels, get_uniq_coin_from_order, get_symbol_price_order_book, main_func

from fastapi_cache.decorator import cache
import time

from fastapi.templating import Jinja2Templates

from cachetools import TTLCache


from starlette.responses import HTMLResponse

# from fastapi_cache.decorator import cache
# import asyncio

# import time
# from fastapi.responses import HTMLResponse 


# from fastapi.encoders import jsonable_encoder 

router = APIRouter(
    prefix='/screener',
    tags=['Фронтэнд']
)


templates = Jinja2Templates(directory='app/templates')





# @router.get('/hotels')
# async def get_impulses(
#     request: Request, 
#     impulses=Depends(get_symbol_tf_impulses)
# ):
#     return templates.TemplateResponse(
#         name='screener.html', 
#         context={'request':request, 'impulses': impulses},
#         )



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
    return templates.TemplateResponse(
        "positions.html", {"request": request}
        )


cache = TTLCache(maxsize=100, ttl=600) 

@router.get('/coin_info/{symbol}/{tf}', response_class=HTMLResponse) 
async def get_coin_info(request: Request, symbol: str, tf: int): 
    # Генерируем уникальный ключ для кэша 
    cache_key = f"{symbol}_{tf}" 

    if cache_key in cache:
        print('беру из кэша')
        html_content = cache[cache_key] 
    else: 
        response = templates.TemplateResponse( 
            name='coin_info.html', 
            context={'request': request, 'symbol': symbol, 'tf': tf}, 
        ) 

        html_content = response.body.decode() 

        cache[cache_key] = html_content

    return HTMLResponse(content=html_content)



# @router.get('/coin_info/{symbol}/{tf}') 
# # @cache(expire=600)
# async def get_coin_info(request: Request, symbol: str, tf: int): 

#     # time.sleep(4)




#     print(templates.TemplateResponse( 
#         name='coin_info.html',  
#         context={'request': request,
#                 'symbol':symbol,'tf':tf}, 
#     ))


#     response = templates.TemplateResponse( 
#         name='coin_info.html',  
#         context={'request': request,
#                 'symbol':symbol,'tf':tf}, 
#     )


#     html_content = response.body.decode()

#     return html_content

#     # return templates.TemplateResponse( 
#     #     name='coin_info.html',  
#     #     context={'request': request,
#     #             'symbol':symbol,'tf':tf}, 
#     # )





# @router.get("") 
# def get_impulses(): 
#     impulse = get_symbol_tf_impulses()
#     return impulse  # Возвращаем список для отображения