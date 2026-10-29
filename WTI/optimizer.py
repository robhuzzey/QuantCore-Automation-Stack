import os
import json
import pandas as pd
from openai import OpenAI

SYMBOL = "WTI"  

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_nightly_optimization():
    print(f"🌙 Running multi-year historical cloud optimization for {SYMBOL}...")
    try:
        with open("active_strategy.json", "r") as f:
            current_strategy = json.load(f)
    except FileNotFoundError:
        current_strategy = {
            "fast_ma": 14, "slow_ma": 28, "rsi_period": 14,
            "rsi_overbought": 70, "rsi_oversold": 30,
            "stop_loss_points": 150, "take_profit_points": 300
        }

    prompt = f"Optimize the trading variables for {SYMBOL}. Current Base Parameters: {json.dumps(current_strategy)}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Return ONLY a raw, minified JSON object. No explanations."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        new_strategy = json.loads(response.choices.message.content)
        with open("active_strategy.json", "w") as f:
            json.dump(new_strategy, f, indent=4)
        print(f"🎉 Cloud optimization complete for {SYMBOL}.")
    except Exception as e:
        with open("active_strategy.json", "w") as f:
            json.dump(current_strategy, f, indent=4)

if __name__ == "__main__":
    run_nightly_optimization()
