import os
import json
import pandas as pd
import MetaTrader5 as mt5
from openai import OpenAI

SYMBOL = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_nightly_optimization():
    print(f"Optimizing {SYMBOL}...")

if __name__ == "__main__":
    run_nightly_optimization()
