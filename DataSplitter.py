
import os  
import pandas as pd  
import numpy as np  
  
def split_forex_data(folder_name, from_symbol, to_symbol, required_suffix="_scrubbed.csv"):  
   # Search for files in the folder  
   file_pattern = f"{from_symbol}_{to_symbol}"
   files = [f for f in os.listdir(folder_name) if f.startswith(f"{file_pattern}") and f.endswith(f"{required_suffix}.csv")]  
  
   # If no files are found, exit  
   if not files:  
      print(f"No files found in {folder_name} matching pattern {file_pattern}*{required_suffix}.csv")  
      return  
  
   # Load the data from the first file (assuming there's only one)  
   file_path = os.path.join(folder_name, files[0])  
   data = pd.read_csv(file_path)  
  
   # Split the data into training, validation, and testing sets  
   train_size = int(0.8 * data.shape[0])  
   val_size = int(0.1 * data.shape[0])  
   train_data = data.iloc[:train_size]  
   val_data = data.iloc[train_size:train_size + val_size]  
   test_data = data.iloc[train_size + val_size:] 
  
   # Define the new file names  
   train_file_name = files[0].replace(f'{required_suffix}.csv', '_train.csv')  
   val_file_name = files[0].replace(f'{required_suffix}.csv', '_val.csv') 
   test_file_name = files[0].replace(f'{required_suffix}.csv', '_test.csv') 
  
   # Save the new data sets to files  
   train_data.to_csv(os.path.join(folder_name, train_file_name), index=False)  
   val_data.to_csv(os.path.join(folder_name, val_file_name), index=False)  
   test_data.to_csv(os.path.join(folder_name, test_file_name), index=False)  
  
   print(f"Data split and saved to {folder_name}: {train_file_name}, {val_file_name}, {test_file_name}")

def split_stock_data(folder_name, symbol, required_suffix="_scrubbed"):  
   # Search for files in the folder  
   files = [f for f in os.listdir(folder_name) if f.startswith(f"{symbol}") and f.endswith(f"{required_suffix}.csv")]  
  
   # If no files are found, exit  
   if not files:  
      print(f"No files found in {folder_name} matching pattern {symbol}*{required_suffix}.csv")  
      return  
  
   # Load the data from the first file (assuming there's only one)  
   file_path = os.path.join(folder_name, files[0])  
   data = pd.read_csv(file_path)
   data = data.rename(columns={"Unnamed: 0":"Date", "1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume":"Volume"})

  
   # Split the data into training, validation, and testing sets  
   train_size = int(0.8 * data.shape[0])  
   val_size = int(0.1 * data.shape[0])
   test_size = data.shape[0] - train_size - val_size
   train_indices = range(test_size + val_size, data.shape[0])  
   val_indices = range(test_size, test_size + val_size)  
   test_indices = range(test_size)  
   train_data = data.iloc[train_indices]  
   val_data = data.iloc[val_indices]  
   test_data = data.iloc[test_indices]  

  
   # Define the new file names  
   train_file_name = files[0].replace(f'{required_suffix}.csv', '_train.csv')  
   val_file_name = files[0].replace(f'{required_suffix}.csv', '_val.csv') 
   test_file_name = files[0].replace(f'{required_suffix}.csv', '_test.csv') 
  
   # Save the new data sets to files  
   train_data.to_csv(os.path.join(folder_name, train_file_name), index=False)  
   val_data.to_csv(os.path.join(folder_name, val_file_name), index=False)  
   test_data.to_csv(os.path.join(folder_name, test_file_name), index=False)  
  
   print(f"Data split and saved to {folder_name}: {train_file_name}, {val_file_name}, {test_file_name}")

# Example usage  
#split_forex_data("forex_daily", "USD", "EUR")