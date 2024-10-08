from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.future import select
from sqlalchemy import JSON, Column, Integer, String, Computed, Date, ForeignKey, TIMESTAMP, Float

from fastapi_cache.decorator import cache

import asyncio





DB_HOST = '10.16.0.2'
DB_PORT = 1234
DB_USER = 'fr3sto'
DB_PASS = 'endorphin25'
DB_NAME = 'Screener'
 
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}' 

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 

class Base(DeclarativeBase):
    pass

class Levels(Base): 
    __tablename__   = 'levels' 
 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    symbol = Column(String, nullable=False) 
    tf = Column(Integer, nullable=False) 
    price = Column(Float, nullable=False) 
    type = Column(Integer, nullable=False) 
    date_start = Column(TIMESTAMP, nullable=False) 




class Impulse(Base): 
    __tablename__  = 'impulse' 
 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    symbol = Column(String, nullable=False) 
    type = Column(String, nullable=False) 
    tf = Column(Integer, nullable=False) 
    price_start = Column(Float, nullable=False) 
    date_start = Column(TIMESTAMP, nullable=False) 
    price_end = Column(Float, nullable=False) 
    date_end = Column(TIMESTAMP, nullable=False) 
    is_open = Column(Integer, nullable=False) 
    down_range = Column(Float, nullable=False) 
    up_range = Column(Float, nullable=False) 





class Orders(Base): 
    __tablename__  = 'all_order_book' 
 
    id = Column(Integer, primary_key=True, autoincrement=True) 
    exchange = Column(String, nullable=False) 
    type_exchange = Column(String, nullable=False) 
    symbol = Column(String, nullable=False) 
    type = Column(String, nullable=False) 
    price = Column(Float, nullable=False) 
    pow = Column(Float, nullable=False) 
    quantity = Column(Float, nullable=False) 
    is_not_mm = Column(Integer, nullable=False) 
    date_start = Column(TIMESTAMP, nullable=False) 
    date_end = Column(TIMESTAMP, nullable=False) 
    date_get = Column(TIMESTAMP, nullable=False)



async def get_symbol_tf_impulses(): 
    async with async_session_maker() as session:  #контекстный менеджер . создает новую 
        #сессию для работы с бд. async_session_maker - это фцнкция врзвращающая сессию для работы
        #с ORM (sqlalchemy)
        async with session.begin(): #этот контекстный менеджер начинает транзакцию 
            result = await session.execute(select(Impulse)) 
            #тут запрос к бд. sql запрс . передаются параметры 
            #await session.execute - выполнят запрос и ожидает пока он не завершится
            return result.scalars().all() 
 
async def get_symbol_price_levels(): 
    async with async_session_maker() as session: 
        async with session.begin(): 
            result = await session.execute(select(Levels)) 
            return result.scalars().all() 
 
async def get_symbol_price_order_book(): 
    async with async_session_maker() as session: 
        async with session.begin(): 
            result = await session.execute(select(Orders)) 
            return result.scalars().all() 
 
async def get_uniq_coin_from_order(): 
    list_of_tuple = await get_symbol_price_order_book()
    only_coin = [elem.symbol for elem in list_of_tuple] 
    set_coin = set(only_coin) 
    return list(set_coin) 
 
async def get_uniq_coin(): 
    list_of_tuple = await get_symbol_tf_impulses() 
    
    only_coin = [elem.symbol for elem in list_of_tuple] 
    set_coin = set(only_coin) 
    return list(set_coin) 
 
async def main_func(): 
    list_of_imp = await get_symbol_tf_impulses() 
    list_of_levels = await get_symbol_price_levels() 
    list_of_ob = await get_symbol_price_order_book() 
    uniq_coin_from_order = await get_uniq_coin_from_order() 
    list_uniq_coin = await get_uniq_coin() 
 
    dict_coin = {elem: {'30': [], '60': []} for elem in list_uniq_coin} 
 
    for imp in list_of_imp: 
        symbol = imp.symbol
        tf = imp.tf
        price_start = imp.price_start
        price_end = imp.price_end
        type_ = imp.type  
        dict_coin[symbol][str(tf)].append('График') 
 
        # Добавляем количество левелс 
        # !!!!!!!!!!!!!!sum_levels = sum(1 for coin, tf_from_level in list_of_levels if coin == symbol and tf_from_level == tf) 
        # dict_coin[symbol][str(tf)].append(sum_levels) 

        sum_levels = sum(1 for elem in list_of_levels if elem.symbol == symbol and elem.tf == tf) 
        dict_coin[symbol][str(tf)].append(sum_levels) 
 
        if symbol not in uniq_coin_from_order: 
            dict_coin[symbol][str(tf)].append(0) 
        else: 
            # !!!!!!!!!!!!!price_in_range = sum(1 for coin_order, price_order in list_of_ob if coin_order == symbol and price_order >= price_start and price_order <= price_end) 
            # dict_coin[symbol][str(tf)].append(price_in_range) 

            price_in_range = sum(1 for elem in list_of_ob if elem.symbol == symbol and elem.price >= price_start and elem.price <= price_end) 
            dict_coin[symbol][str(tf)].append(price_in_range) 
 
        dict_coin[symbol][str(tf)].append(type_) 
 
    await asyncio.sleep(4)  # замените на подходящий вам способ управления задержкой 
    return dict_coin
    
    
if __name__ == '__main__':
    res = asyncio.run(get_uniq_coin_from_order())
    print(res)