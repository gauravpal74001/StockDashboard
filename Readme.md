Real-Time Stock Dashboard
A comprehensive Streamlit-based web application for real-time stock market analysis with technical indicators and interactive visualizations.

🚀 Features
Real-time stock data fetching using Yahoo Finance API

Interactive charts with candlestick and line chart options

Technical indicators including SMA (Simple Moving Average) and EMA (Exponential Moving Average)

Multi-timeframe analysis (1 day, 1 week, 1 month, 1 year, maximum)

Live sidebar prices for major stocks (AAPL, GOOGL, AMZN, MSFT)

Responsive design with wide layout for optimal chart viewing

Historical data tables with comprehensive price information

📋 Prerequisites
Python 3.7+ installed on your system

Internet connection for fetching real-time stock data

Web browser (Chrome recommended for best performance)

🛠️ Installation
1. Clone or Download
bash
# Create project directory
mkdir stock-dashboard
cd stock-dashboard
2. Set Up Virtual Environment (Recommended)
bash
# Create virtual environment
python -m venv stock_dashboard_env

# Activate virtual environment
# Windows:
stock_dashboard_env\Scripts\activate
# macOS/Linux:
source stock_dashboard_env/bin/activate
3. Install Dependencies
bash
pip install streamlit plotly pandas yfinance ta pytz
Or create a requirements.txt file:

text
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
yfinance>=0.2.18
ta>=0.10.2
pytz>=2023.3
Then install:

bash
pip install -r requirements.txt
🚀 Usage
Starting the Application
bash
# Navigate to project directory
cd stock-dashboard

# Activate virtual environment (if using)
stock_dashboard_env\Scripts\activate  # Windows
source stock_dashboard_env/bin/activate  # macOS/Linux

# Run the application
python -m streamlit run stock_dashboard.py
Alternative Launch Method
bash
streamlit run stock_dashboard.py
Expected Output
text
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
📊 How to Use
Basic Operations
Enter ticker symbol in the sidebar (e.g., AAPL, MSFT, GOOGL)

Select time period from dropdown (1d, 1wk, 1mo, 1y, max)

Choose chart type (Candlestick or Line)

Add technical indicators (SMA 20, EMA 20)

Click "Update" to refresh data and generate charts

Features Available
Interactive Charts: Zoom, pan, and hover for detailed information

Real-time Metrics: Current price, change percentage, high/low/volume

Historical Data: Complete OHLCV (Open, High, Low, Close, Volume) data tables

Technical Analysis: Moving averages overlaid on price charts

Live Sidebar: Real-time prices for major tech stocks

📁 Project Structure
text
stock-dashboard/
│
├── stock_dashboard.py          # Main application file
├── requirements.txt            # Python dependencies
├── README.md                  # This file
└── stock_dashboard_env/       # Virtual environment (if created)
🔧 Configuration
Time Period Mappings
1d: 1-minute intervals

1wk: 30-minute intervals

1mo: 1-day intervals

1y: 1-week intervals

max: 1-week intervals

Supported Technical Indicators
SMA 20: 20-period Simple Moving Average

EMA 20: 20-period Exponential Moving Average

🐛 Troubleshooting
Common Issues
"streamlit not recognized" Error:

bash
# Use module syntax instead
python -m streamlit run stock_dashboard.py
Package Installation Issues:

bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install with user flag if permission issues
pip install --user streamlit plotly pandas yfinance ta pytz
Data Fetching Problems:

Ensure stable internet connection

Try different ticker symbols

Check if Yahoo Finance is accessible in your region

PATH Warnings:

Add Python Scripts directory to system PATH

Or use virtual environment to avoid conflicts

Performance Tips
Use shorter time periods (1d, 1wk) for faster loading

Avoid maximum timeframe for intraday analysis

Close unused browser tabs to improve responsiveness

📈 Sample Tickers to Try
AAPL - Apple Inc.

MSFT - Microsoft Corporation

GOOGL - Alphabet Inc.

TSLA - Tesla Inc.

AMZN - Amazon.com Inc.

NVDA - NVIDIA Corporation

META - Meta Platforms Inc.

🛡️ Error Handling
The application includes robust error handling for:

Invalid ticker symbols

Network connectivity issues

Data formatting problems

Missing technical indicator data

Empty datasets

🔄 Stopping the Application
To stop the dashboard:

Press Ctrl+C in the terminal 

deactivate

📝 Notes
Data Source: Yahoo Finance (yfinance library)

Market Hours: Data availability depends on market operating hours

Real-time: Data updates when "Update" button is clicked

Browser Compatibility: Optimized for Chrome, works in Firefox and Edge

