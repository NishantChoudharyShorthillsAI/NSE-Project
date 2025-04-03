import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
 
# URL for NSE Nifty 50 live data
NSE_URL = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/"
}
 
# Fetch NSE data
def fetch_nse_data():
    session = requests.Session()
    response = session.get(NSE_URL, headers=HEADERS)
    data = response.json()
    return data["data"]
 
# Process data
def process_data(nse_data):
    df = pd.DataFrame(nse_data)
    print("Available columns:", df.columns.tolist())  # Debugging step
    
    # Ensure required columns exist
    required_columns = ["symbol", "lastPrice", "dayHigh", "dayLow", "previousClose", "change", "pChange"]
    optional_columns = ["yearHigh", "yearLow", "perChange30d"]  # Updated column names
    
    # Only include existing columns
    selected_columns = [col for col in required_columns + optional_columns if col in df.columns]
    df = df[selected_columns]
    
    return df
 
# Identify top 5 gainers and losers
def find_gainers_losers(df):
    gainers = df.nlargest(5, 'pChange')
    losers = df.nsmallest(5, 'pChange')
    return gainers, losers
 
# Identify stocks 30% below 52-week high
def below_52_week_high(df):
    if "yearHigh" in df.columns:
        condition = df["lastPrice"] <= (0.7 * df["yearHigh"])
        return df[condition].nlargest(5, "yearHigh")
    else:
        print("52-week high data not available")
        return pd.DataFrame()
 
# Identify stocks 20% above 52-week low
def above_52_week_low(df):
    if "yearLow" in df.columns:
        condition = df["lastPrice"] >= (1.2 * df["yearLow"])
        return df[condition].nlargest(5, "yearLow")
    else:
        print("52-week low data not available")
        return pd.DataFrame()
 
# Identify top 5 stocks with highest returns in the last 30 days
def highest_returns_30d(df):
    if "perChange30d" in df.columns:
        return df.nlargest(5, "perChange30d")
    else:
        print("30-day return data not available")
        return pd.DataFrame()
 
# Plot Bar Chart
def plot_gainers_losers(gainers, losers):
    plt.figure(figsize=(10, 5))
    plt.bar(gainers['symbol'], gainers['pChange'], color='green', label='Top 5 Gainers')
    plt.bar(losers['symbol'], losers['pChange'], color='red', label='Top 5 Losers')
    plt.xlabel("Stock")
    plt.ylabel("% Change")
    plt.title("Top 5 Gainers and Losers of the Day")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
 
if __name__ == "__main__":
    nse_data = fetch_nse_data()
    df = process_data(nse_data)
    gainers, losers = find_gainers_losers(df)
    below_52w_high = below_52_week_high(df)
    above_52w_low = above_52_week_low(df)
    top_returns_30d = highest_returns_30d(df)
    
    # Display results
    print("Top 5 Gainers:\n", gainers)
    print("Top 5 Losers:\n", losers)
    print("Stocks 30% below 52-week high:\n", below_52w_high)
    print("Stocks 20% above 52-week low:\n", above_52w_low)
    print("Top 5 Stocks with Highest Returns in Last 30 Days:\n", top_returns_30d)
    
    # Plot graph
    plot_gainers_losers(gainers, losers)
 