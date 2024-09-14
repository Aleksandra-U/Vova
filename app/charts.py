import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta, datetime
from plotly.subplots import make_subplots

from app.database import get_candles_by_symbol_tf, get_impulse_opened, get_levels_by_symbol_tf, get_order_book_by_symbol

def get_df_from_candles(candles):
    df = pd.DataFrame(candles, columns=['id','symbol','tf','Open','High','Low','Close','Volume','Date'])
    df = df.drop(['id','symbol','tf'],axis=1)
    #df['Date'] = df['Date'].apply(lambda x: datetime.fromtimestamp(int(str(x)[0:10])))
    df = df.sort_values(by=['Date'])
    return df

def get_currency_chart_with_impulse(symbol, tf, min_step):
    candles = get_candles_by_symbol_tf(symbol, tf)
    df_candles = get_df_from_candles(candles)
    impulse = get_impulse_opened(symbol, tf)[0]
    levels = get_levels_by_symbol_tf(symbol, tf)
    orders_future = get_order_book_by_symbol(symbol)
    orders_spot = get_order_book_by_symbol(symbol.split('USDT')[0] + '/USDT')
    return get_chart_with_impulse(df_candles, impulse,levels,orders_future,orders_spot, tf,symbol, min_step)



def get_chart_with_impulse(df, impulse,levels,orders_future,orders_spot, tf, symbol, min_step):
    #fig = px.line(df, x = 'Date', y = 'Close')
    
    impulse_start = impulse[5]
    impulse_end = impulse[7]
    impulse_time = (impulse_end - impulse_start).total_seconds() / 60
    df = df[df['Date'] > impulse_start - timedelta(minutes=impulse_time * 2)]

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'])])
    
    
    fig.update_layout(xaxis_rangeslider_visible=False,  template = 'plotly_dark')
    

    dateEnd = impulse[7]
    
    need_type_level = 0
    color = ''
    if impulse[2] == 'L':
        color = 'Green'
        need_type_level = 2
    else:
        color = 'Red'
        need_type_level = 1

    fig.add_shape(type="rect",
                          x0=impulse[5], y0=impulse[4], x1=dateEnd, y1=impulse[6],
                          line=dict(color=color))
    
    symbol = impulse[1]
    type = impulse[2]
    tf = impulse[3]
    price_start = impulse[4]
    price_end = impulse[6]

    down_range = impulse[9]
    up_range = impulse[10]

    fig.add_trace(
        go.Scatter(x=[dateEnd, dateEnd,
                        df['Date'].iloc[-1], df['Date'].iloc[-1], dateEnd],
                    y=[down_range, up_range, up_range, down_range, down_range],
                    line=dict(color='rgba(139,0,255, 0.3)'), fillcolor='rgba(139,0,255, 0.2)',
                    fill="toself", mode='lines'))


    up_price = 0
    down_price = 0

    if type == 'L':
        up_price = price_end
        up_price += up_price * 0.01

        down_price = price_start
    else:
        up_price = price_start

        down_price = price_end
        down_price -= down_price * 0.01
    
    for level in levels:
        price = level[3]
        type = level[4]
        date_start = level[5]

        color = ''
        if type == 1:
            color = 'Red'
        else:
            color = 'Green'
        fig.add_shape(type="line",
                            x0=date_start, y0=price, x1=df['Date'].iloc[-1], y1=price,
                            line=dict(color=color, width=3))
        

    for order in orders_future:
        price = order[5]
        type = order[4]
        date_start = order[9]
        is_not_mm = order[8]

        color = 'Red' if type == 'asks' else 'Green'
        if order[3] == symbol:
            if price < up_price and price > down_price:
                if (order[10] - date_start).total_seconds() / 60 > 30:
                    fig.add_shape(type="line",
                                    x0=date_start, y0=price, x1=df['Date'].iloc[-1], y1=price,
                                    line=dict(color=color, width=3, dash="dash"))
                    diff_mins = (df['Date'].iloc[-1] - date_start).total_seconds() / 2
                    fig.add_annotation(
                        x=date_start + timedelta(seconds=diff_mins),  # Положение аннотации по оси x
                        y=price + min_step,  # Положение аннотации по оси y (можно чуть выше линии)
                        text="future",  # Текст аннотации
                        #showarrow=True,  # Показывать стрелку
                        arrowhead=2,  # Стиль стрелки
                        # ax=0,  # Смещение аннотации по оси x
                        # ay=-30,  # Смещение аннотации по оси y
                        # bgcolor="white",  # Цвет фона аннотации
                        # bordercolor="black",  # Цвет границы аннотации
                        borderwidth=1  # Ширина границы аннотации
                    )
                
    for order in orders_spot:
        price = order[5]
        type = order[4]
        date_start = order[9]
        is_not_mm = order[8]

        color = 'Red' if type == 'asks' else 'Green'
        if order[3] == symbol.split('USDT')[0] + '/USDT':
            if order[5] < up_price and order[5] > down_price:
                if (order[10] - order[9]).total_seconds() / 60 > 30:
                    fig.add_shape(type="line",
                                    x0=date_start, y0=price, x1=df['Date'].iloc[-1], y1=price,
                                    line=dict(color=color, width=3, dash="dash"))
                    
                    diff_mins = (df['Date'].iloc[-1] - date_start).total_seconds() / 2
                    fig.add_annotation(
                        x=date_start + timedelta(seconds=diff_mins),  # Положение аннотации по оси x
                        y=price,  # Положение аннотации по оси y (можно чуть выше линии)
                        text="spot",  # Текст аннотации
                        showarrow=True,  # Показывать стрелку
                        #arrowhead=2,  # Стиль стрелки
                        ax=0,  # Смещение аннотации по оси x
                        #ay=-30,  # Смещение аннотации по оси y
                        # Цвет границы аннотации
                        borderwidth=1  # Ширина границы аннотации
                    )
                    

    return fig.to_html(full_html=False)