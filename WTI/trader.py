import time
import os
import csv
import json
import pandas as pd

SYMBOL = "WTI"          
TIMEFRAME_MINUTES = 15
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
    print(f"🤖 Native Algo Node for {SYMBOL} Online and Calculating...")
    while True:
        strat = load_strategy()
        try:
            trade_logs = pd.read_csv("live_trade_history.csv")
        except FileNotFoundError:
            pass
        time.sleep(5)

if __name__ == "__main__":
    print("🚀 RUNNING INITIAL FIRST-BOOT BACKTEST & BASELINE OPTIMIZATION...")
    try:
        from optimizer import run_nightly_optimization
        run_nightly_optimization()
    except Exception as e:
        print(f"Using factory defaults, startup optimization bypassed: {e}")
    main_loop()
