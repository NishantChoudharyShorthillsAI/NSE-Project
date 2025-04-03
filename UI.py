import streamlit as st
from nse_analysis import fetch_nse_data, process_data, find_gainers_losers, below_52_week_high, above_52_week_low, highest_returns_30d, plot_gainers_losers

# Streamlit UI
st.title("📈 Nifty 50 Stock Analysis Dashboard")

# Fetch and Process Data
nse_data = fetch_nse_data()
df = process_data(nse_data)
gainers, losers = find_gainers_losers(df)
below_52w_high = below_52_week_high(df)
above_52w_low = above_52_week_low(df)
top_returns_30d = highest_returns_30d(df)

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
st.pyplot(plot_gainers_losers(gainers, losers))