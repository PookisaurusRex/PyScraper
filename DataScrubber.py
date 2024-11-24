import pandas as pd  
import os  
  
def process_files(folder_name, required_suffix=None):  
   # Get the list of files in the folder  
   files = os.listdir(folder_name)  
  
   # Loop through each file  
   for file in files:  
      # Check if the file has the required suffix (if specified)  
      if required_suffix and not file.endswith(required_suffix):  
        continue  
  
      # Read the file into a Pandas DataFrame  
      df = pd.read_csv(os.path.join(folder_name, file))  
  
      # Rename the columns  
      df = df.rename(columns={"Unnamed: 0":"Date", "1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume":"Volume"})
      #df = df.drop(columns=[0], errors='ignore')  
  
      # Create a copy of the file with the suffix "_scrubbed"  
      if required_suffix:  
        scrubbed_file_name = file.replace(required_suffix, '_scrubbed.csv')  
      else:  
        scrubbed_file_name = file.replace('.csv', '_scrubbed.csv')  
  
      scrubbed_df = df.copy()  
  
      # Add moving average columns  
      scrubbed_df['MA_5'] = scrubbed_df['Close'].rolling(window=5).mean()  
      scrubbed_df['MA_10'] = scrubbed_df['Close'].rolling(window=10).mean()  
      scrubbed_df['MA_20'] = scrubbed_df['Close'].rolling(window=20).mean()

      # Add exponential moving average columns  
      scrubbed_df['EMA_5'] = scrubbed_df['Close'].ewm(span=5, adjust=False).mean()  
      scrubbed_df['EMA_10'] = scrubbed_df['Close'].ewm(span=10, adjust=False).mean()  
      scrubbed_df['EMA_20'] = scrubbed_df['Close'].ewm(span=20, adjust=False).mean()  
  
      # Add relative strength index (RSI) column  
      delta = scrubbed_df['Close'].diff(1)  
      up, down = delta.copy(), delta.copy()  
      up[up < 0] = 0  
      down[down > 0] = 0  
      roll_up = up.ewm(com=13-1, adjust=False).mean()  
      roll_down = down.ewm(com=13-1, adjust=False).mean().abs()  
      RS = roll_up / roll_down  
      RSI = 100.0 - (100.0 / (1.0 + RS))  
      scrubbed_df['RSI'] = RSI  
  
      # Add Bollinger Bands columns  
      scrubbed_df['BB_Middle'] = scrubbed_df['Close'].rolling(window=20).mean()  
      scrubbed_df['BB_Upper'] = scrubbed_df['BB_Middle'] + 2*scrubbed_df['Close'].rolling(window=20).std()  
      scrubbed_df['BB_Lower'] = scrubbed_df['BB_Middle'] - 2*scrubbed_df['Close'].rolling(window=20).std()  

      # Add Ichimoku Cloud indicator 
      scrubbed_df['Conversion Line'] = (scrubbed_df['High'].rolling(window=9).max() + scrubbed_df['Low'].rolling(window=9).min()) / 2  
      scrubbed_df['Base Line'] = (scrubbed_df['High'].rolling(window=26).max() + scrubbed_df['Low'].rolling(window=26).min()) / 2  
      scrubbed_df['Leading Span A'] = (scrubbed_df['Conversion Line'] + scrubbed_df['Base Line']) / 2  
      scrubbed_df['Leading Span B'] = (scrubbed_df['High'].rolling(window=52).max() + scrubbed_df['Low'].rolling(window=52).min()) / 2    
  
      # Remove the index column from the saved file
      scrubbed_df.reset_index(drop=True, inplace=True)

      # Save the scrubbed file  
      scrubbed_df.to_csv(os.path.join(folder_name, scrubbed_file_name), index=False)  
  
process_files('stock_daily', required_suffix='_daily_json.csv')  
#process_files('forex_intraday', required_suffix='_cleaned.csv')  
#process_files('forex_daily', required_suffix='_cleaned.csv')