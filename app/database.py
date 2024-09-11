from psycopg2 import pool
from sshtunnel import SSHTunnelForwarder

from fastapi_cache.decorator import cache
# from fastapi.encoders import jsonable_encoder 

import time

server =  SSHTunnelForwarder(
    ('31.129.99.176', 22), #Remote server IP and SSH port
    ssh_username = "root",
    ssh_password = "Endorphin25)",
    remote_bind_address=('localhost', 1234),
    local_bind_address=('localhost', 1234)) #PostgreSQL server IP and sever port on remote machine
        
server.start()   

postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
                                                         password="endorphin25",
                                                         host=server.local_bind_host,
                                                         port=server.local_bind_port,
                                                         database="Screener")

# postgreSQL_pool = pool.ThreadedConnectionPool(1, 100, user="fr3sto",
#                                                          password="endorphin25",
#                                                          host='10.16.0.2',
#                                                          port=1234,
#                                                          database="Screener")

# GET

def get_all_currency():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Currency')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    postgreSQL_pool.putconn(connection)

    symbols_ob = dict()

    for curr in result:
        exchange = curr[1]
        type = curr[2]
        symbol = curr[3]
        min_step = curr[4]
        
        if not exchange in symbols_ob:
            symbols_ob[exchange] = dict()
        
        if not type in symbols_ob[exchange]:
            symbols_ob[exchange][type] = dict()

        symbols_ob[exchange][type][symbol] = {'min_step':float(min_step)}

        
    return symbols_ob



def get_all_impulses():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Impulse')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result



def get_status():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * from Status_Service')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_candles_by_symbol_tf(symbol,tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Candles where Symbol = %s and TF = %s',(symbol,tf))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_impulse_opened(symbol, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Impulse Where Symbol = %s and TF = %s', (symbol, tf))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Order_Book')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_order_book_by_symbol(symbol):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM All_Order_Book WHERE Symbol = %s',(symbol,))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_all_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Levels')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result

def get_levels_by_symbol_tf(symbol, tf):
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Levels Where Symbol = %s and TF = %s', (symbol, tf))
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result






































#взяла из импульсов монеты, tf, цену начало, цену конец
def get_symbol_tf_impulses(): 
    connection = postgreSQL_pool.getconn() 
    cursor = connection.cursor() 
    cursor.execute('SELECT symbol, tf, price_start, price_end, type FROM Impulse') 
    result = cursor.fetchall() 
    cursor.close() 
    postgreSQL_pool.putconn(connection) 
    return result





#получаю все уникальные монеты 
def get_uniq_coin():
    list_of_tuple = get_symbol_tf_impulses()

    only_coin = []
    for elem in list_of_tuple:
        only_coin.append(elem[0])

    set_coin = set(only_coin)
    to_list = list(set_coin)
    return to_list





# сортирую монеты по папкам времени 
def get_sort_by_ft():
    list_of_tuple = get_symbol_tf_impulses()
    f_5 = []
    f_15 = []
    f_30 = []
    f_60 = []
    for elem in list_of_tuple:
        if elem[1] == 5:
            f_5.append(elem[0])
        if elem[1] == 15:
            f_15.append(elem[0])
        if elem[1] == 30:
            f_30.append(elem[0])
        if elem[1] == 60:
            f_60.append(elem[0])

    all_list = []
    all_list.append(f_5)
    all_list.append(f_15)
    all_list.append(f_30)
    all_list.append(f_60)

    return all_list




#беру из левелс список кортежей в которых монета и tf 
def get_symbol_price_levels():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT symbol, tf FROM Levels')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result



#смотрю сколько каждой монеты в левелс 
def amount_coin_in_levels():
    list_of_tuple = get_symbol_price_levels()
    coin_count = {} 
    
    for coin, price in list_of_tuple: 
        if coin in coin_count: 
            coin_count[coin] += 1 
        else: 
            coin_count[coin] = 1 
            
    return coin_count







#беру из ордер монеты и цену 
def get_symbol_price_order_book():
    connection = postgreSQL_pool.getconn()
    cursor = connection.cursor()
    cursor.execute('SELECT symbol, price FROM All_Order_Book')
    result = cursor.fetchall()
    cursor.close()
    postgreSQL_pool.putconn(connection)
    return result




#смотрю какие есть уникальные монеты в ордер 
def get_uniq_coin_from_order():
    list_of_tuple = get_symbol_price_order_book()

    only_coin = []
    for elem in list_of_tuple:
        only_coin.append(elem[0])

    set_coin = set(only_coin)
    to_list = list(set_coin)
    return to_list


#type = 'L', 'S'

@cache(expire=600)
async def main_func():
    list_of_imp = get_symbol_tf_impulses() #тут symbol, tf, price_start, price_end из импульсов
    list_of_levels = get_symbol_price_levels() #список кортежей в которых монета и цена из левелсов 
    list_of_ob = get_symbol_price_order_book() #беру из ордер монеты и цену 
    uniq_coin_from_order = get_uniq_coin_from_order () 

#список уникальных монет 
    list_uniq_coin=get_uniq_coin()

    dict_coin = {}

    for elem in list_uniq_coin:
        dict_coin [elem] = {'5': [], '15': [], '30': [], '60': []} #в каждом [] график, количество левелс, сколько монет в ордер которые входят в диапозон


    #ключом будут уникальные монеты. значением будет другой словарь, ключи в нем: 5, 15, 30, 60. значение 
    #слово график, количество левелс, сколько монет в ордер которые входят в диапозон 
    for imp in list_of_imp:
        symbol = imp[0]
        tf = imp[1]
        price_start = imp[2]
        price_end = imp[3]
        type = imp[4]
        # если есть импульс (монета с таким tf). то добавяю в значение словаря
        dict_coin[symbol][str(tf)].append('График')

        # 2. если есть такой импульс, проеряю есть ли левелс с такой монетой у которой такой tf. 
        # добавляю количетво таких левелс 
        sum_levels = 0
        for coin, tf_from_level in list_of_levels: #список кортежей в которых монета и tf  
            if coin == symbol and tf_from_level == tf:
                sum_levels += 1
        dict_coin[symbol][str(tf)].append(sum_levels)

        # 3. проверяю затем есть ли эта монета в ордер. если нет - пишу 0 в словарь.
        if symbol not in uniq_coin_from_order:
                dict_coin[symbol][str(tf)].append(0)

        #  если есть монета взять все такие монеты и их цены. и проверяю находит ся ли 
        # цена в диапозне price start and price end. смотрю, что цены > price_start и < price_end. 
        # если находится в диапозоне. считаю. переменная + 1        
        else:        
            price_in_range = 0
            for coin_order, price_order in list_of_ob:
                if coin_order == symbol:
                    if price_order >= price_start and price_order <= price_end:
                        price_in_range +=1 
            dict_coin[symbol][str(tf)].append(price_in_range)    


        dict_coin[symbol][str(tf)].append(type)


    time.sleep(4)

    return dict_coin


