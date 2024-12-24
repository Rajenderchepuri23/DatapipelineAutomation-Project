import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging #automation runs in the background and logs helps you to trouble shoot 
import schedule
import time
from database import create_table,insert_stock_data


API_KEY ='KU4XP3T7OEIEWQFG'
BASE_URL ="https://www.alphavantage.co/query"


#FETCH THE DATA NOW

def fetch_stock_data(symbol):
    params={
        'function' : 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey' : API_KEY
    }
    #print("Sending API Request...")
    try:
        logging.info(f"Fetching data for {symbol}....")
    except Exception as e:
        logging.error(f"failed to fecth data for {symbol: {e}}")
    response = requests.get(BASE_URL,params=params)
    if response.status_code == 200:
        print("API Response Received.")
        data = response.json()
        
        # Check for specific errors in the API response
        if "Error Message" in data:
            print(f"Error: {data['Error Message']}")
            return None
        elif "Time Series (5min)" not in data:
            print("Error: 'Time Series (5min)' not found in the API response.")
            return None
        
        return data
    else:
        logging.error(f"Failed to fetch data for {symbol}. HTTP Status Code: {response.status_code}")
        return None
    

    #function for processing the data into a dataframe from json

def process_data(raw_data):
    """
    Process the raw API response to extract relevant data and convert it into a DataFrame.
    """
    try:

       # Extract the "Time Series (5min)" data
        time_series_data = raw_data.get("Time Series (5min)")

        if not time_series_data:


            logging.error("Error: 'Time Series (5min)' not found in the API response.")
            return None

        # Convert the nested dictionary to a DataFrame
        df = pd.DataFrame.from_dict(time_series_data, orient="index")
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Data processing failed. Expected a DataFrame but got something else.")


        # Rename columns to meaningful names
        df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }, inplace=True)

        # Reset index to make the timestamps a column
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Timestamp"}, inplace=True)
        #df["Timestamp"] = df["Timestamp"].dt.tz_localize('US/Central')  # Convert to the API's timezone
       # df["Timestamp"] = df["Timestamp"].dt.tz_convert('') 

        # Convert data types for numerical operations and visualization
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["Open"] = pd.to_numeric(df["Open"])
        df["High"] = pd.to_numeric(df["High"])
        df["Low"] = pd.to_numeric(df["Low"])
        df["Close"] = pd.to_numeric(df["Close"])
        df["Volume"] = pd.to_numeric(df["Volume"])
        logging.info("Data processed into DataFrame successfully.")


        return df

    except Exception as e:
        logging.error(f"An error occurred while processing the data: {e}")
        return None

def saving_tocsv(df,symbol):
    if isinstance(df,pd.DataFrame):
        try:

            filename =f"Data for {symbol}_stock_data.csv"
            df.to_csv(filename,index=False)
            logging.info(f"data for {symbol} saved to {filename}")
        except Exception as e:
            logging.error(f"failed to save data for {symbol}:{e}")
    else:
            logging.error("Provided data is not a DataFrame. Skipping save")
    
def fetch_favstock(favourite_stocks):
    for stock in favourite_stocks:
        raw_data=fetch_stock_data(stock)
        if raw_data:
            stock_data =process_data(raw_data)
        if stock_data is not None:
            insert_stock_data(stock,stock_data)
            saving_tocsv(stock,stock_data)
            print(f"Data for {stock} processed and inserted.")
        else:
            print(f"Failed to process data for {stock}.")
        

def fetch_dynamicstock():
    symbol =input('Enter the stock synbol to fetch data : ').strip().upper()
    raw_data=fetch_stock_data(symbol)
    if raw_data:
        stock_data =process_data(raw_data)
        if  isinstance(stock_data, pd.DataFrame):
            insert_stock_data(symbol,stock_data)
            vis_stock_data(stock_data,symbol)
        else:
            print("failed to process stock data")
            logging.error("Failed to process stock data into a DataFrame.")
    else:
        print("failed to fetch stock data")
        logging.error("Failed to fecth stock data into a DataFrame.")

def vis_stock_data(df,symbol):
    try:
        plt.figure(figsize=(14,7))
        plt.plot(df['Timestamp'],df['Open'],label='Open',linestyle='--')
        plt.plot(df['Timestamp'],df['High'],label='High',linestyle='-.')
        plt.plot(df['Timestamp'],df['Low'],label='Low',linestyle=':')
        plt.plot(df['Timestamp'],df['Close'],label='Close',linewidth=2)

        plt.title(f"Stock Prices for {symbol}", fontsize=16)  # Adds a title to the chart.
        plt.xlabel("Timestamp", fontsize=14)  # X-axis label for time.
        plt.ylabel("Price (USD)", fontsize=14)  # Y-axis label for prices.
        plt.legend(fontsize=12)  # Add a legend to identify different lines.
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        logging.info(f"Visualization for {symbol} was successful.")
    
    except Exception as e:
        logging.error(f"Failed to visualize stock data for {symbol}: {e}")
        print(f"An error occurred while visualizing data for {symbol}. Check the logs for details.")



if __name__ == "__main__":
    create_table()
    favourite_stocks =['AAPL','GOOGL','MSFT','TSLA']
    schedule.every(5).minutes.do(fetch_favstock,favourite_stocks)
    print("Automation is running. Press Ctrl+C to stop.")
    print("You can also fetch data for any stock dynamically.")
    while True:
        
            user_input = input("Type 'fetch' to get a stock or 'wait' to continue automation: ").strip().lower()
            if user_input == 'fetch':
                
                fetch_dynamicstock()
            elif user_input == 'wait':
                print("Automation is running. Waiting for the next scheduled task...")
                while True:
                    try:
                        schedule.run_pending()
                        print("Scheduled tasks are running... (Press Ctrl+C to stop)")
                        time.sleep(1)
                    except KeyboardInterrupt:

                        print("\nStopping automation...")
                        break
        







