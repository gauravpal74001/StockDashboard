# Source: @DeepCharts Youtube Channel (https://www.youtube.com/@DeepCharts)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

##########################################################################################
## PART 1: Define Functions for Pulling, Processing, and Creating Technical Indicators ##
##########################################################################################

# Fetch stock data based on the ticker, period, and interval
def fetch_stock_data(ticker, period, interval):
    try:
        end_date = datetime.now()
        if period == '1wk':
            start_date = end_date - timedelta(days=7)
            data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        else:
            data = yf.download(ticker, period=period, interval=interval)
        
        # Ensure data is properly structured
        if not data.empty and len(data.columns.levels) > 1:
            # Handle multi-level columns that sometimes occur with yfinance
            data.columns = data.columns.droplevel(1)
        
        return data
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Process data to ensure it is timezone-aware and has the correct format
def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    
    # Ensure all numeric columns are properly formatted
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_columns:
        if col in data.columns:
            data[col] = data[col].squeeze()  # Remove extra dimensions
    
    return data

# Calculate basic metrics from the stock data - FIXED VERSION
def calculate_metrics(data):
    # Convert Series to scalar values using .iloc and float()
    last_close = float(data['Close'].iloc[-1])
    prev_close = float(data['Close'].iloc[0])
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = float(data['High'].max())
    low = float(data['Low'].min())
    volume = int(data['Volume'].sum())
    return last_close, change, pct_change, high, low, volume

# Add simple moving average (SMA) and exponential moving average (EMA) indicators
def add_technical_indicators(data):
    try:
        # Ensure Close column is 1-dimensional
        close_prices = data['Close'].squeeze()
        
        # Calculate indicators with proper error handling
        data['SMA_20'] = ta.trend.sma_indicator(close_prices, window=20)
        data['EMA_20'] = ta.trend.ema_indicator(close_prices, window=20)
        
        return data
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        # Return data without indicators if calculation fails
        data['SMA_20'] = None
        data['EMA_20'] = None
        return data


# Creating the Dashboard App layout ##


# Set up Streamlit page layout
st.set_page_config(layout="wide")
st.title('Real Time Stock Dashboard')

# 2A: SIDEBAR PARAMETERS ############

# Sidebar for user input parameters
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'ADBE')
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

# Mapping of time periods to data intervals
interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}

# 2B: MAIN CONTENT AREA ############

# Update the dashboard based on user input - FIXED VERSION
if st.sidebar.button('Update'):
    try:
        data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
        
        # Check if data is empty
        if data.empty:
            st.error(f"No data available for {ticker} in the selected time period.")
        else:
            data = process_data(data)
            data = add_technical_indicators(data)
            
            last_close, change, pct_change, high, low, volume = calculate_metrics(data)
            
            # Display main metrics - Now using scalar values
            st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("High", f"{high:.2f} USD")
            col2.metric("Low", f"{low:.2f} USD")
            col3.metric("Volume", f"{volume:,}")
            
            # Plot the stock price chart
            fig = go.Figure()
            if chart_type == 'Candlestick':
                fig.add_trace(go.Candlestick(x=data['Datetime'],
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close']))
            else:
                fig = px.line(data, x='Datetime', y='Close')
            
            # Add selected technical indicators to the chart
            for indicator in indicators:
                if indicator == 'SMA 20':
                    fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20'))
                elif indicator == 'EMA 20':
                    fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))
            
            # Format graph
            fig.update_layout(title=f'{ticker} {time_period.upper()} Chart',
                              xaxis_title='Time',
                              yaxis_title='Price (USD)',
                              height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display historical data and technical indicators
            st.subheader('Historical Data')
            st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])
            
            st.subheader('Technical Indicators')
            st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])
            
    except Exception as e:
        st.error(f"Error updating dashboard: {str(e)}")
        st.info("Please try a different ticker symbol or time period.")

# 2C: SIDEBAR PRICES ############

# Sidebar section for real-time stock prices of selected symbols - FIXED VERSION
st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
for symbol in stock_symbols:
    try:
        real_time_data = fetch_stock_data(symbol, '1d', '1m')
        if not real_time_data.empty:
            real_time_data = process_data(real_time_data)
            
            # Fix: Extract scalar values properly
            last_price = float(real_time_data['Close'].iloc[-1])
            first_price = float(real_time_data['Open'].iloc[0])
            change = last_price - first_price
            pct_change = (change / first_price) * 100
            
            st.sidebar.metric(f"{symbol}", f"{last_price:.2f} USD", f"{change:.2f} ({pct_change:.2f}%)")
    except Exception as e:
        st.sidebar.error(f"Error loading {symbol}: {str(e)}")

# Sidebar information section
st.sidebar.subheader('About')
st.sidebar.info('This dashboard provides stock data and technical indicators for various time periods. Use the sidebar to customize your view.')
