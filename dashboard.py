import streamlit as st
import pandas as pd
import json
import glob
import os
import yfinance as yf

st.set_page_config(layout="wide", page_title="AI Quant Command Station", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    html, body, [data-testid="stWidgetLabel"], .stText, p, li {
        font-size: 20px !important;
        font-weight: 500 !important;
        color: #e0e0e0 !important;
    }
    h1 {
        font-size: 46px !important;
        font-weight: 800 !important;
        color: #FFD700 !important;
        margin-bottom: 0px !important;
    }
    h2 {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    h3 {
        font-size: 24px !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 54px !important;
        font-weight: 900 !important;
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 18px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        color: #888888 !important;
    }
    .stDataFrame, table, th, td {
        font-size: 18px !important;
        font-family: 'Courier New', monospace !important;
    }
    th {
        background-color: #111111 !important;
        color: #FFD700 !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .param-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 HERMES PORTFOLIO CONTROL STATION")

if "run_count" not in st.session_state:
    st.session_state.run_count = 0
st.session_state.run_count += 1

SYMBOL_MAP = {"XAUUSD": "GC=F", "WTI": "CL=F", "XAGUSD": "SI=F"}
asset_dirs = [d for d in glob.glob("*/") if os.path.exists(os.path.join(d, "active_strategy.json"))]
total_pnl = 0.0
all_history = []
asset_pnl_breakdown = {}
live_prices = {}
active_strategies = {}

for folder in asset_dirs:
    asset_name = folder.replace("/", "").replace("\\", "")
    asset_pnl_breakdown[asset_name] = 0.0
    
    try:
        yf_ticker = SYMBOL_MAP.get(asset_name, "GC=F")
        ticker_df = yf.download(yf_ticker, period="1d", interval="5m", progress=False, auto_adjust=True)
        if not ticker_df.empty:
            if isinstance(ticker_df.columns, pd.MultiIndex):
                ticker_df.columns = ticker_df.columns.get_level_values(0)
            live_prices[asset_name] = ticker_df
    except Exception:
        pass

    try:
        strategy_file = os.path.join(folder, "active_strategy.json")
        if os.path.exists(strategy_file):
            with open(strategy_file, "r") as f:
                active_strategies[asset_name] = json.load(f)
            
        history_file = os.path.join(folder, "live_trade_history.csv")
        if os.path.exists(history_file):
            node_df = pd.read_csv(history_file)
            if not node_df.empty and len(node_df.columns) > 1:
                node_pnl = pd.to_numeric(node_df['profit']).sum()
                total_pnl += node_pnl
                asset_pnl_breakdown[asset_name] = node_pnl
                all_history.append(node_df)
    except Exception:
        pass

col1, col2, col3 = st.columns(3)
col1.metric(label="Real Account Equity", value=f"${10000.0 + total_pnl:,.2f}", delta=f"${total_pnl:+.2f}" if total_pnl != 0 else None)
col2.metric(label="Computational Engines", value=len(asset_dirs))
col3.metric(label="Telemetry Syncs", value=f"#{st.session_state.run_count}")

st.markdown("<hr>", unsafe_allow_html=True)

st.header("🗂️ Active Performance Allocation & Real-Time Price Streams")
breakdown_cols = st.columns(len(asset_pnl_breakdown) if len(asset_pnl_breakdown) > 0 else 1)

for idx, (asset, pnl) in enumerate(asset_pnl_breakdown.items()):
    with breakdown_cols[idx]:
        st.subheader(f"🌐 Node: {asset}")
        
        if asset in live_prices and not live_prices[asset].empty:
            close_series = live_prices[asset]["Close"].squeeze().dropna()
            current_price = float(close_series.iloc[-1])
            st.metric(label="Live Exchange Price", value=f"${current_price:,.2f}")
            st.line_chart(close_series.tail(25), height=180, use_container_width=True)
        else:
            st.warning("Connecting to exchange feed...")
            
        if asset in active_strategies:
            s = active_strategies[asset]
            st.markdown(f"""
            <div class='param-box'>
                <b>🎯 Strategy Config</b><br>
                • MA Crossover: {s.get('fast_ma', 14)} / {s.get('slow_ma', 28)}<br>
                • RSI Window: {s.get('rsi_period', 14)} (Oversold: {s.get('rsi_oversold', 30)} / Overbought: {s.get('rsi_overbought', 70)})
            </div>
            """, unsafe_allow_html=True)
            
        st.metric(label="Realised Yield (PnL)", value=f"${pnl:,.2f}")

st.markdown("<hr><br>", unsafe_allow_html=True)

st.header("📈 Real-Time Execution Order History (Demo Account)")
if all_history and len(all_history) > 0:
    combined_df = pd.concat(all_history).sort_values(by="timestamp", ascending=False)
    st.dataframe(combined_df, use_container_width=True, hide_index=True)
else:
    st.info("Awaiting entry criteria triggers... No active positions open.")

st.components.v1.html(
    """
    <script>
    setTimeout(function(){
        window.parent.location.reload();
    }, 60000);
    </script>
    """,
    height=0
)
