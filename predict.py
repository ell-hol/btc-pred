import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse

# Model parameters and genesis block date
C = 1.60e-18
k = 6.04
genesis_block_date = datetime(2009, 1, 3)

def load_data(csv_path):
    data = pd.read_csv(csv_path)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def predict_bitcoin_prices(start_year, end_year, month):
    start_date = f"{start_year}-{month:02d}-01"
    end_date = datetime(end_year, month, 1) + pd.offsets.MonthEnd(1)
    date_range = pd.date_range(start=start_date, end=end_date)
    days_since_genesis = (date_range - genesis_block_date).days
    predicted_prices = C * days_since_genesis**k
    predictions_df = pd.DataFrame({'Date': date_range, 'Predicted Price (USD)': predicted_prices})
    return predictions_df

def plot_predictions(btc_data, predictions):
    plt.figure(figsize=(10, 6))
    plt.yscale('log')
    if btc_data is not None:
        plt.plot(btc_data['Date'], btc_data['Close'], label='Historical Prices')
    plt.plot(predictions['Date'], predictions['Predicted Price (USD)'], label='Predicted Prices')
    plt.xlabel('Year')
    plt.ylabel('Price (USD)')
    plt.title('Bitcoin Price Predictions')
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Generate Bitcoin price predictions.")
    parser.add_argument("--csv", "-c", type=str, help="Path to the CSV file containing historical Bitcoin prices.")
    parser.add_argument("--year", "-y", type=int, help="Start year for which to predict prices.")
    parser.add_argument("--month", "-m", type=int, help="Month for which to predict prices.")
    parser.add_argument("--plot", action='store_true', help="Plot predictions along with historical data.")
    args = parser.parse_args()

    btc_data = None
    if args.csv:
        btc_data = load_data(args.csv)
    
    if args.plot:
        # Assuming the historical data contains a 'Price' column
        predictions = predict_bitcoin_prices(2014, args.year + 25, args.month)
        plot_predictions(btc_data, predictions)
    else:
        predictions = predict_bitcoin_prices(args.year, args.year, args.month)
        print(predictions)

if __name__ == "__main__":
    main()
