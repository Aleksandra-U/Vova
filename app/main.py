from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


from contextlib import asynccontextmanager


# from app.screener.router import router as router_screener

from app.pages.router import router as router_impulses



@asynccontextmanager
async def lifespan(_: FastAPI):
    #redis = aioredis.from_url("redis://localhost")
    # redis_port=6379
    redis = aioredis.from_url("redis://redis")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

# app = FastAPI()

app.include_router(router_impulses)



# app.include_router(router_screener)

# @app.get('/Vov')
# def get_data():
#     return 'Сайт для Вовы'





# import asyncssh 
# import asyncio 
# from fastapi import FastAPI, APIRouter 
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker 
# from sqlalchemy.orm import sessionmaker 
# from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, select 
# from sqlalchemy.ext.declarative import declarative_base 
 
# # Настройки SSH 
# SSH_HOST = 'your_ssh_server'  # ваш SSH сервер 
# SSH_USER = 'your_ssh_username'  # ваш SSH пользователь 
# SSH_PASSWORD = 'your_ssh_password'  # ваш SSH пароль 
# LOCAL_BIND_IP = '127.0.0.1' 
# LOCAL_BIND_PORT = 5432  # Порт на локальном хосте 
# REMOTE_DB_HOST = '127.0.0.1'  # Хост базы данных на удаленном сервере 
# REMOTE_DB_PORT = 5432  # Порт базы данных на удаленном сервере 
 
# # Данные для подключения к базе данных 
# DB_USER = 'fr3sto' 
# DB_PASS = 'endorphin' 
# DB_NAME = 'Screener' 
 
# # Создание базы данных 
# Base = declarative_base() 
 
# class Levels(Base): 
#     tablename = 'levels' 
 
#     id = Column(Integer, primary_key=True, autoincrement=True) 
#     symbol = Column(String, nullable=False) 
#     tf = Column(Integer, nullable=False) 
#     price = Column(Float, nullable=False) 
#     type = Column(Integer, nullable=False) 
#     date_start = Column(TIMESTAMP, nullable=False) 
 
# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{LOCAL_BIND_IP}:{LOCAL_BIND_PORT}/{DB_NAME}' 
 
# # Создание движка и сессии 
# engine = create_async_engine(DATABASE_URL, echo=True) 
# async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession) 
 
# app = FastAPI() 
# router = APIRouter() 
 
# async def start_ssh_tunnel(): 
#     async with asyncssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD) as conn: 
#         await conn.forward_local_port(LOCAL_BIND_IP, LOCAL_BIND_PORT, REMOTE_DB_HOST, REMOTE_DB_PORT) 
#         await conn.wait_closed()  # Поддерживаем соединение открытым 
 
# @app.on_event("startup") 
# async def startup_event(): 
#     # Запуск SSH туннеля 
#     asyncio.create_task(start_ssh_tunnel()) 
 
# @router.get("/levels") 
# async def get_levels(): 
#     async with async_session_maker() as session: 
#         query = select(Levels) 
#         result = await session.execute(query) 
#         levels = result.scalars().all()  # Получаем все результаты 
#         return levels 
 
# app.include_router(router) 