import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

class NSEStockAnalyzer:
    NSE_URL = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }
    
    def __init__(self):
        self.data_frame = None
    
    def fetch_data(self):
        session = requests.Session()
        response = session.get(self.NSE_URL, headers=self.HEADERS)
        data = response.json()
        return data["data"]
    
    def process_data(self, data):
        df = pd.DataFrame(data)
        print("Available columns:", df.columns.tolist())  # Debugging step
        
        required_columns = ["symbol", "lastPrice", "dayHigh", "dayLow", "previousClose", "change", "pChange"]
        optional_columns = ["yearHigh", "yearLow", "perChange30d"]
        
        selected_columns = [col for col in required_columns + optional_columns if col in df.columns]
        self.data_frame = df[selected_columns]
    
    def find_gainers_losers(self):
        gainers = self.data_frame.nlargest(5, 'pChange')
        losers = self.data_frame.nsmallest(5, 'pChange')
        return gainers, losers
    
    def below_52_week_high(self):
        if "yearHigh" in self.data_frame.columns:
            condition = self.data_frame["lastPrice"] <= (0.7 * self.data_frame["yearHigh"])
            return self.data_frame[condition].nlargest(5, "yearHigh")
        print("52-week high data not available")
        return pd.DataFrame()
    
    def above_52_week_low(self):
        if "yearLow" in self.data_frame.columns:
            condition = self.data_frame["lastPrice"] >= (1.2 * self.data_frame["yearLow"])
            return self.data_frame[condition].nlargest(5, "yearLow")
        print("52-week low data not available")
        return pd.DataFrame()
    
    def highest_returns_30d(self):
        if "perChange30d" in self.data_frame.columns:
            return self.data_frame.nlargest(5, "perChange30d")
        print("30-day return data not available")
        return pd.DataFrame()
    
    def plot_gainers_losers(self, gainers, losers):
        plt.figure(figsize=(10, 5))
        plt.bar(gainers['symbol'], gainers['pChange'], color='green', label='Top 5 Gainers')
        plt.bar(losers['symbol'], losers['pChange'], color='red', label='Top 5 Losers')
        plt.xlabel("Stock")
        plt.ylabel("% Change")
        plt.title("Top 5 Gainers and Losers of the Day")
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()
    
    def analyze(self):
        data = self.fetch_data()
        self.process_data(data)
        gainers, losers = self.find_gainers_losers()
        below_52w_high = self.below_52_week_high()
        above_52w_low = self.above_52_week_low()
        top_returns_30d = self.highest_returns_30d()
        
        print("Top 5 Gainers:\n", gainers)
        print("Top 5 Losers:\n", losers)
        print("Stocks 30% below 52-week high:\n", below_52w_high)
        print("Stocks 20% above 52-week low:\n", above_52w_low)
        print("Top 5 Stocks with Highest Returns in Last 30 Days:\n", top_returns_30d)
        
        self.plot_gainers_losers(gainers, losers)

if __name__ == "__main__":
    analyzer = NSEStockAnalyzer()
    analyzer.analyze()
# This script fetches stock data from the NSE India website, processes it, and performs analysis