#import Scraper
#import DataScrubber
#import Cleaner
import DataSplitter
#import MetadataAnalyzer1

from alpaca.trading.client import TradingClient
from DataSplitter import split_stock_data as SplitStockData

bPaperAccount = True

with open('alpaca_api_key.txt', 'r') as f:  
    alpaca_api_key = f.read().strip()

with open('alpaca_secret_key.txt', 'r') as f:  
    alpaca_secret_key = f.read().strip()

trading_client = TradingClient(alpaca_api_key, alpaca_secret_key)

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

SplitStockData("stock_daily", "HAL", required_suffix="_daily_json")