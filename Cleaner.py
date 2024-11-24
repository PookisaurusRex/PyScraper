import pandas as pd  
import os  
  
def CleanAndNormalizeData(folder_name, impute_missing_values=False, excluded_suffix=['_scrubbed.csv', '_cleaned.csv', "_train.csv", "_test.csv", "_val.csv"]):  
    # Get the list of files in the folder  
    files = os.listdir(folder_name)
    for suffix in excluded_suffix:
        files = [file for file in files if not file.endswith(suffix)]
    # Loop through each file  
    for file in files:  
        # Read the file into a Pandas DataFrame  
        df = pd.read_csv(os.path.join(folder_name, file))  
  
        # Impute missing values if specified  
        if impute_missing_values:  
            df.infer_objects(copy=False)
            df.interpolate(method='linear', limit_direction='both', inplace=True)
  
        # Clean and normalize the data  
        clean_df = CleanAndNormalize_df(df)
        
        # Save the cleaned data to a new file  
        new_file_name = file.replace('_scrubbed.csv', '_cleaned.csv')  
        clean_df.to_csv(os.path.join(folder_name, new_file_name), index=False)  
  
def CleanAndNormalize_df(df):
    bFirst = True;
    for col in df.columns:  
        # Skip the index column  
        if bFirst: bFirst = False; continue;
        min_values = df[col].min()  
        max_values = df[col].max()  
  
        # Normalize the data  
        df[col] = (df[col] - min_values) / (max_values - min_values)

    df.dropna(inplace=True)
  
    # Return the normalized DataFrame with the original index  
    return df
  
#CleanAndNormalizeData('forex_intraday', impute_missing_values=True)  
#CleanAndNormalizeData('forex_daily', impute_missing_values=True)
CleanAndNormalizeData('stock_daily', impute_missing_values=True, excluded_suffix=["_daily_json.csv", "_train.csv", "_test.csv", "_val.csv"])