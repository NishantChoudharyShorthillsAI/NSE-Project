import streamlit as st
from nse_analysis import NSEStockAnalyzer

# Streamlit UI
st.title("📈 Nifty 50 Stock Analysis Dashboard")

# Create Analyzer Instance
analyzer = NSEStockAnalyzer()
analyzer.analyze()

gainers, losers = analyzer.find_gainers_losers()
below_52w_high = analyzer.below_52_week_high()
above_52w_low = analyzer.above_52_week_low()
top_returns_30d = analyzer.highest_returns_30d()

# Display Data in Streamlit
st.subheader("📊 Top 5 Gainers")
st.dataframe(gainers)

st.subheader("📉 Top 5 Losers")
st.dataframe(losers)

st.subheader("📌 Stocks 30% Below 52-Week High")
st.dataframe(below_52w_high)

st.subheader("🚀 Stocks 20% Above 52-Week Low")
st.dataframe(above_52w_low)

st.subheader("🔥 Top 5 Stocks with Highest Returns in Last 30 Days")
st.dataframe(top_returns_30d)

# Display Chart
st.subheader("📊 Gainers & Losers Chart")
st.pyplot(analyzer.plot_gainers_losers(gainers, losers))
