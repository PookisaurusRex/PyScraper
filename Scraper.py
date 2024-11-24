import requests  
import json  
import pandas as pd  
from datetime import datetime, timedelta  
import logging  
import time  
import os  
  
# Set up logging  
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  
  
# Global currencies array  
CURRENCIES = ['USD', 'EUR', 'JPY', 'GBP', 'CNY', 'CAD']  
  
def scrape_alpha_vantage_forex_intraday(from_symbol, to_symbol, interval, outputsize='compact', datatype='json'):  
   logging.info(f'Scraping intraday data for {from_symbol}/{to_symbol} with interval {interval}...')  
   # Read API key from file  
   with open('alpha_vantage_key.txt', 'r') as f:  
      api_key = f.read().strip()  
  
   # Construct API URL  
   url = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&outputsize={outputsize}&datatype={datatype}&apikey={api_key}'  
  
   # Send GET request to API  
   response = requests.get(url)  
  
   # Check if response was successful  
   if response.status_code == 200:  
      logging.info(f'Received response from API for {from_symbol}/{to_symbol} with interval {interval}...')  
      # Parse JSON response  
      data = json.loads(response.text)  
  
      # Check if response is empty  
      if not data:  
        logging.warning(f'Empty response from API for {from_symbol}/{to_symbol} with interval {interval}')  
        return None  
  
      # Check if response has missing data  
      if 'Time Series FX (1min)' not in data:  
        logging.warning(f'Missing data in response from API for {from_symbol}/{to_symbol} with interval {interval}')  
        return None  
  
      # Extract the "Time Series FX (1min)" data  
      ts_data = data['Time Series FX (1min)']  
  
      # Create a Pandas DataFrame from the data  
      df = pd.DataFrame(ts_data).T  
  
      return df  
   else:  
      logging.error(f'Error scraping intraday data for {from_symbol}/{to_symbol} with interval {interval}: {response.status_code}')  
      if response.text:  
        logging.error(f'Response: {response.text}')  
      return None  
  
def scrape_alpha_vantage_forex_daily(from_symbol, to_symbol, outputsize='compact', datatype='json'):  
   logging.info(f'Scraping daily data for {from_symbol}/{to_symbol}...')  
   # Read API key from file  
   with open('alpha_vantage_key.txt', 'r') as f:  
      api_key = f.read().strip()  
  
   # Construct API URL  
   url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_symbol}&to_symbol={to_symbol}&outputsize={outputsize}&datatype={datatype}&apikey={api_key}'  
  
   # Send GET request to API  
   response = requests.get(url)  
  
   # Check if response was successful  
   if response.status_code == 200:  
      logging.info(f'Received response from API for {from_symbol}/{to_symbol}...')  
      # Parse JSON response  
      data = json.loads(response.text)  
  
      # Check if response is empty  
      if not data:  
        logging.warning(f'Empty response from API for {from_symbol}/{to_symbol}')  
        return None  
  
      # Check if response has missing data  
      if 'Time Series FX (Daily)' not in data:  
        logging.warning(f'Missing data in response from API for {from_symbol}/{to_symbol}')  
        return None  
  
      # Extract the "Time Series FX (Daily)" data  
      ts_data = data['Time Series FX (Daily)']  
  
      # Create a Pandas DataFrame from the data  
      df = pd.DataFrame(ts_data).T  
  
      return df  
   else:  
      logging.error(f'Error scraping daily data for {from_symbol}/{to_symbol}: {response.status_code}')  
      if response.text:  
        logging.error(f'Response: {response.text}')  
      return None  
  
def save_response_to_csv(response, from_symbol, to_symbol, interval, datatype):  
   # Convert the response to a pandas DataFrame  
   df = pd.DataFrame(response)  
  
   # Create a filename based on the input parameters  
   filename = f"{from_symbol}_{to_symbol}_{interval}_{datatype}_raw.csv"  
  
   # Create the "forex_intraday" folder if it doesn't exist  
   folder_path = "forex_intraday"  
   if not os.path.exists(folder_path):  
      os.makedirs(folder_path)  
  
   # Save the DataFrame to a CSV file in the "forex_data" folder  
   df.to_csv(os.path.join(folder_path, filename), index=True)  
  
def save_daily_response_to_csv(response, from_symbol, to_symbol, datatype):  
   # Convert the response to a pandas DataFrame  
   df = pd.DataFrame(response)  
  
   # Create a filename based on the input parameters  
   filename = f"{from_symbol}_{to_symbol}_daily_{datatype}_raw.csv"  
  
   # Create the "forex_daily" folder if it doesn't exist  
   folder_path = "forex_daily"  
   if not os.path.exists(folder_path):  
      os.makedirs(folder_path)  
  
   # Save the DataFrame to a CSV file in the "forex_data" folder  
   df.to_csv(os.path.join(folder_path, filename), index=True)  
  
def scrape_all_intraday_combinations(interval, outputsize='compact', datatype='json', throttle=75):  
   logging.info(f'Scraping all intraday combinations for interval {interval} with throttle {throttle} calls/minute...')  
   calls_made = 0  
   start_time = time.time()  
   for from_symbol in CURRENCIES:  
      for to_symbol in CURRENCIES:  
        if from_symbol != to_symbol:  
           # Check if we need to wait due to throttle  
           if calls_made >= throttle:  
              elapsed_time = time.time() - start_time  
              if elapsed_time < 60:  
                wait_time = 60 - elapsed_time  
                logging.info(f'Waiting {wait_time:.2f} seconds to respect throttle...')  
                time.sleep(wait_time)  
              start_time = time.time()  
              calls_made = 0  
  
           data = scrape_alpha_vantage_forex_intraday(from_symbol, to_symbol, interval, outputsize, datatype)  
           if data is not None and not data.empty:  
              logging.info(f'Creating DataFrame for {from_symbol}/{to_symbol} with interval {interval}...')  
  
              # Create a file name based on the parameters  
              file_name = f'{from_symbol}_{to_symbol}_{interval}_{datatype}.csv'  
  
              # Create the "forex_intraday" folder if it doesn't exist  
              folder_path = "forex_intraday"  
              if not os.path.exists(folder_path):  
                os.makedirs(folder_path)  
  
              # Check if the file already exists  
              try:  
                # If the file exists, read it into a Pandas DataFrame  
                existing_df = pd.read_csv(file_name)  
                # Merge the new data with the existing data  
                df = pd.concat([existing_df, data])  
              except FileNotFoundError:  
                # If the file doesn't exist, create a new one  
                df = data  
  
              # Remove duplicated intervals from the merged data  
              df = df.drop_duplicates(keep='first')  
  
              # Save the merged data to the file  
              logging.info(f'Saving data to {file_name}...')  
              # Save the DataFrame to a CSV file in the "forex_data" folder  
              df.to_csv(os.path.join(folder_path, file_name), index=True)  
              logging.info(f'Data saved to {file_name}')  
  
           calls_made += 1  
  
def scrape_all_daily_combinations(outputsize='compact', datatype='json', throttle=75):  
   logging.info(f'Scraping all daily combinations with throttle {throttle} calls/minute...')  
   calls_made = 0  
   start_time = time.time()  
   for from_symbol in CURRENCIES:  
      for to_symbol in CURRENCIES:  
        if from_symbol != to_symbol:  
           # Check if we need to wait due to throttle  
           if calls_made >= throttle:  
              elapsed_time = time.time() - start_time  
              if elapsed_time < 60:  
                wait_time = 60 - elapsed_time  
                logging.info(f'Waiting {wait_time:.2f} seconds to respect throttle...')  
                time.sleep(wait_time)  
              start_time = time.time()  
              calls_made = 0  
  
           data = scrape_alpha_vantage_forex_daily(from_symbol, to_symbol, outputsize, datatype)  
           if data is not None and not data.empty:  
              logging.info(f'Creating DataFrame for {from_symbol}/{to_symbol}...')  
  
              # Create a file name based on the parameters  
              file_name = f'{from_symbol}_{to_symbol}_daily_{datatype}.csv'  
  
              # Create the "forex_daily" folder if it doesn't exist  
              folder_path = "forex_daily"  
              if not os.path.exists(folder_path):  
                os.makedirs(folder_path)  
  
              # Check if the file already exists  
              try:  
                # If the file exists, read it into a Pandas DataFrame  
                existing_df = pd.read_csv(file_name)  
                # Merge the new data with the existing data  
                df = pd.concat([existing_df, data])  
              except FileNotFoundError:  
                # If the file doesn't exist, create a new one  
                df = data  
  
              # Remove duplicated intervals from the merged data  
              df = df.drop_duplicates(keep='first')  
  
              # Save the merged data to the file  
              logging.info(f'Saving data to {file_name}...')  
              # Save the DataFrame to a CSV file in the "forex_data" folder  
              df.to_csv(os.path.join(folder_path, file_name), index=True)  
              logging.info(f'Data saved to {file_name}')  
  
           calls_made += 1  

def scrape_daily_stock_data(ticker, outputsize='compact', datatype='json'):  
   logging.info(f'Scraping daily data for stock {ticker}...')  
   # Read API key from file  
   with open('alpha_vantage_key.txt', 'r') as f:  
      api_key = f.read().strip()  
  
   # Construct API URL  
   url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}&outputsize={outputsize}&datatype={datatype}'  
  
   # Send GET request to API  
   response = requests.get(url)  
  
   # Check if response was successful  
   if response.status_code == 200:  
      logging.info(f'Received response from API for stock {ticker}...')  
      # Parse JSON response
      data = json.loads(response.text)  
  
      # Check if response is empty  
      if not data:  
        logging.warning(f'Empty response from API for stock {ticker}')  
        return None  
  
      # Check if response has missing data  
      if 'Time Series (Daily)' not in data:  
        logging.warning(f'Missing data in response from API for stock {ticker}')  
        return None  
  
      # Extract the "Time Series (Daily)" data  
      ts_data = data['Time Series (Daily)']  
  
      # Create a Pandas DataFrame from the data  
      df = pd.DataFrame(ts_data).T  
  
      # Create a file name based on the parameters  
      file_name = f'{ticker}_daily_{datatype}.csv'
  
      # Create the "forex_daily" folder if it doesn't exist  
      folder_path = "stock_daily"  
      if not os.path.exists(folder_path):  
        os.makedirs(folder_path)  
  
      # Save the data to the file  
      logging.info(f'Saving data to {file_name}...')  
      df.to_csv(os.path.join(folder_path, file_name), index=True)  
      logging.info(f'Data saved to {file_name}')  
  
      return df  
   else:  
      logging.error(f'Error scraping data for stock {ticker}: {response.status_code}')  
      if response.text:  
        logging.error(f'Response: {response.text}')  
      return None  
  
# Example usage:  
#scrape_daily_stock_data('VTRS', 'full', 'json')
#scrape_daily_stock_data('F', 'full', 'json')
#scrape_daily_stock_data('AMCR', 'json')
#scrape_daily_stock_data('PCG', 'json')
#scrape_daily_stock_data('HPE', 'json')
#scrape_daily_stock_data('T', 'json')
#scrape_daily_stock_data('KEY', 'json')
#scrape_daily_stock_data('INTC', 'json')
#scrape_daily_stock_data('PFE', 'json')
#scrape_daily_stock_data('HAL', 'full', 'json')
#scrape_daily_stock_data('LUV', 'json')
#scrape_daily_stock_data('SMCI', 'json')
#scrape_daily_stock_data('MRO', 'json')
#scrape_daily_stock_data('HRL', 'json')
#scrape_daily_stock_data('KDP', 'json')
#scrape_daily_stock_data('KHC', 'json')
#scrape_daily_stock_data('PLTR', 'json')

#scrape_all_intraday_combinations('1min', 'full')  
#scrape_all_daily_combinations('full')