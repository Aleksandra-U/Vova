from pydantic_settings import BaseSettings
from pydantic import BaseModel, model_validator

class Settings(BaseSettings):
    user: str
    password: str
    remote_host: str
    remote_port: int
    db_host: str
    db_port: int
    dbname='Screener'


    # dbname='Screener',
    # user = 'fr3sto',
    # password='endorphin25',
    # host=server.local_bind_host,
    # port=server.local_bind_port

    DATABASE_URL: str = None

    @model_validator(mode='before')
    def get_database_url(cls, values):
        values['DATABASE_URL'] = f'postgresql+asyncpg://{values["DB_USER"]}:{values["DB_PASS"]}@{values["DB_HOST"]}:{values["DB_PORT"]}/{values["DB_NAME"]}'
        return values



    class Config:
        env_file = '.env'

settings = Settings()

# Опционально, вывод DATABASE_URL для проверки
# print(f'DATABASE_URL: {settings.user}:{settings.password}@{settings.db_host}:{settings.db_port}')