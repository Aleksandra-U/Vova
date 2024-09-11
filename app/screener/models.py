# from app.databaseNO import Base
# from sqlalchemy import JSON, Column, Integer, String, Computed, Date, ForeignKey, TIMESTAMP, Float


# class Levels(Base): 
#     __tablename__  = 'levels' 
 
#     id = Column(Integer, primary_key=True, autoincrement=True) 
#     symbol = Column(String, nullable=False) 
#     tf = Column(Integer, nullable=False) 
#     price = Column(Float, nullable=False) 
#     type = Column(Integer, nullable=False) 
#     date_start = Column(TIMESTAMP, nullable=False) 




# class Impulse(Base): 
#     __tablename__ = 'impulse' 
 
#     id = Column(Integer, primary_key=True, autoincrement=True) 
#     symbol = Column(String, nullable=False) 
#     type = Column(String, nullable=False) 
#     tf = Column(Integer, nullable=False) 
#     price_start = Column(Float, nullable=False) 
#     date_start = Column(TIMESTAMP, nullable=False) 
#     price_end = Column(Float, nullable=False) 
#     date_end = Column(TIMESTAMP, nullable=False) 
#     is_open = Column(Integer, nullable=False) 
#     down_range = Column(Float, nullable=False) 
#     up_range = Column(Float, nullable=False) 





# class Orders(Base): 
#     __tablename__ = 'orders' 
 
#     id = Column(Integer, primary_key=True, autoincrement=True) 
#     exchange = Column(String, nullable=False) 
#     type_exchange = Column(String, nullable=False) 
#     symbol = Column(String, nullable=False) 
#     type = Column(String, nullable=False) 
#     price = Column(Float, nullable=False) 
#     pow = Column(Float, nullable=False) 
#     quantity = Column(Float, nullable=False) 
#     is_not_mm = Column(Integer, nullable=False) 
#     date_start = Column(TIMESTAMP, nullable=False) 
#     date_end = Column(TIMESTAMP, nullable=False) 
#     date_get = Column(TIMESTAMP, nullable=False)








#     # __tablename__ = 'bookings'

#     # id = Column(Integer, primary_key= True) 
#     # room_id = Column(ForeignKey('rooms.id'))
#     # user_id = Column(ForeignKey('users.id'))
#     # date_from = Column(Date, nullable=False)
#     # date_to = Column(Date, nullable=False)
#     # price = Column(Integer, nullable=False)
#     # total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
#     # total_deys = Column(Integer, Computed('date_to - date_from'))
