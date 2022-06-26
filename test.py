import pandas as pd
import datetime
from alpaca_trade_api import REST, TimeFrame

Ticker = 'tsla'
interval = 10
Start = (datetime.datetime.now()-datetime.timedelta(days=interval)).strftime('%Y-%m-%d')
End = (datetime.datetime.now()).strftime('%Y-%m-%d')
api = REST('PKWZ3J8AEQYSBJVKK1MW',
'1r7TUmFUlnETLAdlTtzUeJcJqYXaldCWygC21GQK')
stock_data = api.get_bars(Ticker, TimeFrame.Minute,Start,End,adjustment='raw',).df

import matplotlib.pyplot as plt

stock_data['open']

stock_data['open'] - stock_data['vwap']
