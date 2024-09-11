# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
# import asyncio
# import asyncssh

# from sshtunnel import SSHTunnelForwarder #Run pip install sshtunnel


# class Base(DeclarativeBase):
#     pass



# # Настройки подключения SSH и БД 
# ssh_user = 'fr3sto' 
# ssh_password = 'endorphin25' 
# ssh_host = settings.ssh_host  # например, 'your.ssh.server' 
# ssh_port = 22  # стандартный порт SSH 

# db_host = server.local_bind_host 
# db_port = server.local_bind_port  # стандартный порт для MySQL 
# db_name = 'Screener' 
# db_user = 'fr3sto' 
# db_pass = 'pass'



# # Установка SSH туннеля 
# server = SSHTunnelForwarder( 
#     (ssh_host, ssh_port), 
#     ssh_username=ssh_user, 
#     ssh_password=ssh_password, 
#     remote_bind_address=(db_host, db_port), 
# ) 
 
# # Запускаем сервер 
# server.start() 
 
# # Создаем асинхронный движок SQLAlchemy 
# engine = create_async_engine( 
#     f'mysql+mysqldb://{db_user}:{db_pass}@127.0.0.1:{server.local_bind_port}/{db_name}' 
# ) 
 
# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 
 
 
# async def get_async_session() -> AsyncSession: 
#     async with async_session_maker() as session: 
#         yield session 
 
 
# # Не забудьте остановить туннель при завершении работы приложения 
# import atexit 
# atexit.register(server.stop)
















# # server =  SSHTunnelForwarder(
# #     user='fr3sto',
# #     password='endorphin',
# #     host=server.local_bind_host,
# #     port=server.local_bind_port,
# #     dbname='Screener',)




# # server.start()

# # engine = create_async_engine('mysql+mysqldb://user:pass@127.0.0.1:%s/db' % server.local_bind_port)

# # async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# # server.stop()









# # server =  SSHTunnelForwarder(
# #         ('31.129.99.176', 22), #Remote server IP and SSH port
# #         ssh_username = "root",
# #         ssh_password = "Endorphin25)",
# #         remote_bind_address=('localhost', 1234),
# #         local_bind_address=('localhost', 1234)) #PostgreSQL server IP and sever port on remote machine
            
# # server.start() #start ssh sever


# # user='fr3sto',
# # password='endorphin',
# # host=server.local_bind_host,
# # port=server.local_bind_port,
# # dbname='Screener',

# # DATABASE_URL = f'postgresql+asyncpg://{user}:{password}@{host}:{1234}/{dbname}'




# # engine = create_async_engine(DATABASE_URL,echo=True)

# # async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)



# # class Base(DeclarativeBase):
# #     pass









# # async def create_ssh_tunnel(): 
# #     user = settings.user 
# #     password = settings.password 
# #     remote_host = settings.remote_host 
# #     remote_port = settings.remote_port 
# #     db_host = settings.db_host 
# #     db_port = settings.db_port 
 
# #     # Создаем SSH-туннель  
# #     conn = await asyncssh.connect(remote_host, username=user, password=password, known_hosts=None)  
# #     #await conn.start_local_port_forwarding('localhost', db_port, remote_host, remote_port) 
 
# #     return conn  # Возвращаем соединение для использования





# # async def create_async_engine_with_tunnel():   
# #     # Создаем SSH-туннель   
# #     conn = await create_ssh_tunnel() 
# #     try: 
# #         database_url = f'postgresql+asyncpg://{settings.user}:{settings.password}@localhost:{settings.db_port}/Screener'   
# #         engine = create_async_engine(database_url, echo=True)   
# #         return engine 
# #     finally: 
# #         #await conn.stop_local_port_forwarding(settings.db_port)  # Закрываем туннель 
# #         conn.close()  # Закрываем соединение



# # async def get_async_session():  
# #     engine = await create_async_engine_with_tunnel()  
# #     async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  
# #     async with async_session_maker() as session:  
# #         return session





# # async def create_ssh_tunnel():
# #     user = settings.user
# #     password = settings.password
# #     remote_host = settings.remote_host
# #     remote_port = settings.remote_port
# #     db_host = settings.db_host
# #     db_port = settings.db_port
    


# #     # Создаем SSH-туннель  
# #     # conn = await asyncssh.connect(remote_host, username=user, password=password, known_hosts=None) 
# #     # await conn.start_local_port_forwarding('localhost', db_port, remote_host, remote_port) 
     
# #     # try:  
# #     #     return conn  # Возвращаем соединение для использования 
# #     # finally: 
# #     #     await conn.stop_local_port_forwarding(db_port)   # Закрываем соединение (это будет выполнено в функции выше) 
 

# #     # Создаем SSH-туннель 
# #     async with asyncssh.connect(remote_host, username=user, password=password, known_hosts=None) as conn: 
# #         # Открываем туннель 
# #         await conn.start_local_port_forwarding('localhost', db_port, remote_host, remote_port) 
# #         try: 
# #             yield 
# #         finally: 
# #             await conn.stop_local_port_forwarding(db_port)  # Закрываем туннель 




# # async def create_async_engine_with_tunnel():  
# #     # Создаем SSH-туннель  
# #     conn = await create_ssh_tunnel()  
# #     database_url = f'postgresql+asyncpg://{settings.user}:{settings.password}@localhost:{settings.db_port}/Screener'  
# #     engine = create_async_engine(database_url, echo=True)  
# #     return engine  

 
# # async def get_async_session():  
# #     engine = await create_async_engine_with_tunnel()  
# #     async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  
# #     async with async_session_maker() as session:  
# #         return session