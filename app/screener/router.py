# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# # from app.databaseNO import get_async_session
# # from app.screener.models import Levels, Impulse, Orders
# from app.database import get_all_levels

# router = APIRouter(
#     prefix='/screener',
#     tags=['Screener'],
# )



# @router.get("") 
# async def get_levels(): 
#     levels = get_all_levels()
#     return levels  # Возвращаем список для отображения




# # # @router.get("") 
# # # async def get_levels(session: AsyncSession = Depends(get_async_session)): 
# # #     query = select(Levels) 
# # #     result = await session.execute(query) 
# # #     levels = result.scalars().all()  # Получаем результаты в виде списка объектов Levels 
# # #     return levels  # Возвращаем список для отображения





# # # @router.get("") 
# # # async def get_levels(): 
# # #     async with async_session_maker() as session:  # Используем ее с контекстным менеджером 
# # #         query = select(Levels) 
# # #         result = await session.execute(query) 
# # #         print(result)
# #         # levels = result.scalars().all()  # Извлекаем все результаты 
# #         # return levels  # Возвращаем полученные данные
              

# # # @router.get("") 
# # # async def get_levels():
# # #     async with get_async_session() as session:
# # #         query = select(Levels)
# # #         result = await session.execute(query)
# # #         print(result)



# # # @router.get("") 
# # # async def get_levels(session: AsyncSession = Depends(get_async_session)): 
# # #     result = await session.execute(select(Levels)) 
# # #     levels = result.scalars().all() 
# # #     return levels