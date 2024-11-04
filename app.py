import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import ta.momentum
import ta.trend
import ta.volatility
import yfinance as yf
import datetime as dt
import ta

project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.append(project_root)


today = dt.datetime.today()
st.session_state.refresh_speed = None
interval_second = None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_old_data(ticker: str) -> pd.DataFrame:
    yesterday_date = today - dt.timedelta(hours=8)
    yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')
    data = yf.download(ticker, start="2024-01-01", end=yesterday_date_str, prepost=False)
    try:
        data = data.droplevel('Ticker', axis=1)
    except:
        print("No Ticker level")
        
    data.index = pd.to_datetime(data.index)
    data['date'] = data.index.date
    return data

def fetch_latest_data(ticker: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    latest_data = stock.history(interval='1m', period='1d', prepost=True)[-1:]
    latest_data['date'] = latest_data.index.date
    return latest_data

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    data['EMA10'] = ta.trend.EMAIndicator(data["Close"], window=10).ema_indicator()
    data['rsi'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    boll = ta.volatility.BollingerBands(data['Close'])
    data['bollh'] = boll.bollinger_hband()
    data['bolll'] = boll.bollinger_lband()
    return data

def create_rsi_figure(data: pd.DataFrame):
    layout = go.Layout(
        title=f'RSI',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value'),
        width=800,
        height=400,
        uirevision=True  # This prevents the UI from resetting
    )
    fig = go.Figure(layout=layout)

    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rsi'],
        mode="lines",
        name="RSI",
        line=dict(color='orange')
    ))

    fig.add_hrect(y0=0, y1=30, line_width=0, fillcolor="red", opacity=0.2)
    fig.add_hrect(y0=70, y1=100, line_width=0, fillcolor="red", opacity=0.2)

    fig.update_yaxes(range=[0,100])
    return fig
    
    

def create_price_figure(data: pd.DataFrame, ticker: str):
    layout = go.Layout(
        title=f'{ticker} Price Chart',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        width=800,
        height=600,
        uirevision=True  # This prevents the UI from resetting
    )
    
    fig = go.Figure(layout=layout)
    
    fig.add_trace(go.Candlestick(
        x=data['date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Price"
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['EMA10'],
        mode="lines",
        name="EMA10",
        line=dict(color='orange')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['bollh'],
        mode="lines",
        name="Bollinger High",
        line=dict(color='rgba(0,255,0,0.3)')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['bolll'],
        mode="lines",
        name="Bollinger Low",
        line=dict(color='rgba(255,0,0,0.3)')
    ))
    
    # Add range slider
    fig.update_layout(xaxis_rangeslider_visible=True)
    
    return fig




def main() -> None:
    st.title("Real Time Stock Price")

    col1 , col2 = st.columns(2)
    with col1:
        ticker = st.text_input(label='Ticker', value="MSFT", label_visibility='collapsed')
    with col2:
        st.button("search")

    speed = st.select_slider(
        "Select a speed for refresh",
        options=[
            "Never",
            "Slow",
            "Medium",
            "Fast"
        ],
    )

    if speed =='Never':
        st.session_state.refresh_speed = None
    elif speed =='Slow':
        st.session_state.refresh_speed = 60
    elif speed =='Medium':
        st.session_state.refresh_speed = 20
    elif speed =='Fast':
        st.session_state.refresh_speed = 5

    # Reset session state if ticker changes
    if st.session_state.last_ticker != ticker:
        st.session_state.data = None
        st.session_state.price_fig = None
        st.session_state.rsi_fig = None
        st.session_state.last_ticker = ticker
    
    # Initial data load
    if st.session_state.data is None:
        old_data = fetch_old_data(ticker)
        st.session_state.data = old_data

    @st.fragment(run_every=st.session_state.refresh_speed)
    def update_data(ticker:str):
        global today
        if today.date() !=dt.datetime.today().date():
            today = dt.datetime.today()
            st.rerun()

        latest_data = fetch_latest_data(ticker)
        # # Combine old and new data
        data = pd.concat([
            st.session_state.data[['date', 'Open', 'High', 'Low', 'Close']],
            latest_data[['date', 'Open', 'High', 'Low', 'Close']]
        ], ignore_index=True)
        
        # Calculate indicators
        data_with_indicators = calculate_indicators(data)
        print(data_with_indicators[-2:])
        st.session_state.lastet_data_indicators = data_with_indicators;


    @st.fragment(run_every=st.session_state.refresh_speed)
    def show_price_chart(ticker):
        
        if 'lastet_data_indicators' in st.session_state:
            data = st.session_state.lastet_data_indicators

            if st.session_state.price_fig==None :
                st.session_state.price_fig = create_price_figure(data, ticker)
            else:
                with st.session_state.price_fig.batch_update():
                    st.session_state.price_fig.data[0].close = data['Close'][:]
                    st.session_state.price_fig.data[0].high = data['High'][:]
                    st.session_state.price_fig.data[0].low = data['Low'][:]
                    st.session_state.price_fig.data[0].open = data['Open'][:]
                    st.session_state.price_fig.data[0].x = data['date'][:]

                    st.session_state.price_fig.data[1].y = data['EMA10'][:]
                    st.session_state.price_fig.data[1].x = data['date'][:]

                    st.session_state.price_fig.data[2].y = data['bollh'][:]
                    st.session_state.price_fig.data[2].x = data['date'][:]

                    st.session_state.price_fig.data[3].y = data['bolll'][:]
                    st.session_state.price_fig.data[3].x = data['date'][:]

            st.plotly_chart(st.session_state.price_fig, use_container_width=True)

    @st.fragment(run_every=st.session_state.refresh_speed)
    def show_rsi_chart():

        if 'lastet_data_indicators' in st.session_state:
            data = st.session_state.lastet_data_indicators

            if st.session_state.rsi_fig == None:
                st.session_state.rsi_fig = create_rsi_figure(data)
            else:
                with st.session_state.rsi_fig.batch_update():
                    st.session_state.rsi_fig.data[0].y = data['rsi'][:]


        st.plotly_chart(st.session_state.rsi_fig, use_container_width=True)

    @st.fragment(run_every=st.session_state.refresh_speed)
    def show_detail():
        #show_price_chart(ticker=ticker,price_container=price_container)
        #st.line_chart(data=data, x='date', y=['rsi'])
        st.write(f"""
        Latest Price: {st.session_state.lastet_data_indicators['Close'].iloc[-1]:.2f}
        
        Recent Data:
        """)
        print(st.session_state.lastet_data_indicators)
        st.dataframe(st.session_state.lastet_data_indicators[-2:])

    update_data(ticker)
    show_price_chart(ticker)
    show_rsi_chart()
    show_detail()
    print(st.session_state.refresh_speed)




if __name__ == '__main__':
    # Initialize session state
    print(today.date())
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'price_fig' not in st.session_state:
        st.session_state.price_fig = None
    if 'rsi_fig'  not in st.session_state:
        st.session_state.rsi_fig = None
    if 'last_ticker' not in st.session_state:
        st.session_state.last_ticker = None
    main()