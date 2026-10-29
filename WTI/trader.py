import time
import os
import csv
import json
import MetaTrader5 as mt5
import pandas as pd

SYMBOL = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
TIMEFRAME = mt5.TIMEFRAME_M15
STARTING_EQUITY = 10000.0  
MAX_DAILY_DRAWDOWN_PCT = 0.05 

def load_strategy():
    with open("active_strategy.json", "r") as f:
        return json.load(f)

def log_trade(ticket, order_type, price, profit, slippage, spread):
    file_exists = os.path.isfile("live_trade_history.csv")
    with open("live_trade_history.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "ticket", "symbol", "type", "price", "profit", "slippage", "spread"])
        writer.writerow([time.time(), ticket, SYMBOL, order_type, price, profit, slippage, spread])

def main_loop():
    if not mt5.initialize():
        print(f"MT5 Node Failure for {SYMBOL}")
        return
    print(f"🤖 Algo Node for {SYMBOL} Online and Streaming Data...")
    while True:
        account_info = mt5.account_info()
        if account_info is None:
            time.sleep(1)
            continue
        if account_info.equity < (STARTING_EQUITY * (1 - MAX_DAILY_DRAWDOWN_PCT)):
            print(f"🚨 CIRCUIT BREAKER TRIGGERED FOR {SYMBOL}. Closing exposures.")
            mt5.Close(symbol=SYMBOL)
            break
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
