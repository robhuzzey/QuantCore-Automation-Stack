import streamlit as st
import pandas as pd
import json
import glob
import os

st.set_page_config(layout="wide", page_title="Quant Core Terminal", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0c10 !important;
    }
    html, body, [data-testid="stWidgetLabel"], .stText, p, li {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    h1 {
        font-size: 46px !important;
        font-weight: 900 !important;
        color: #ffffff !important; 
        margin-bottom: 25px !important;
        border-bottom: 3px solid #1f2833;
        padding-bottom: 12px;
        letter-spacing: -0.5px;
    }
    h2 {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #909caf !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        font-size: 64px !important;
        font-weight: 900 !important;
        color: #00ffcc !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 18px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        color: #909caf !important;
        letter-spacing: 1px;
    }
    .stDataFrame, table, th, td {
        font-size: 22px !important;
        font-family: 'Courier New', monospace !important;
    }
    th {
        background-color: #1f2833 !important;
        color: #00ffcc !important;
        font-weight: 900 !important;
        padding: 14px !important;
        border: 2px solid #45a29e !important;
    }
    td {
        background-color: #151922 !important;
        color: #ffffff !important;
        padding: 14px !important;
        border: 1px solid #1f2833 !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .pnl-card {
        background-color: #151922;
        padding: 24px;
        border-radius: 8px;
        border: 3px solid #45a29e;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    }
    .cfd-name {
        color: #ff9f1c !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        display: block;
        margin-bottom: 8px;
        border-bottom: 1px solid #1f2833;
        padding-bottom: 4px;
    }
    header, [data-testid="stHeader"], .stAppDeployButton {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎛️ COLD TRADING CORE TERMINAL")

if "run_count" not in st.session_state:
    st.session_state.run_count = 0
st.session_state.run_count += 1

asset_dirs = [d for d in glob.glob("*/") if os.path.exists(os.path.join(d, "active_strategy.json"))]
total_pnl = 0.0
all_history = []
asset_pnl_breakdown = {}

for folder in asset_dirs:
    asset_name = folder.replace("/", "").replace("\\", "")
    asset_pnl_breakdown[asset_name] = 0.0
    try:
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

col_cap1, col_cap2, col_cap3 = st.columns(3)
col_cap1.metric(label="Total Portfolio Capital", value=f"${10000.0 + total_pnl:,.2f}", delta=f"${total_pnl:+.2f}" if total_pnl != 0 else None)
col2_metric = col_cap2.metric(label="Active CFD Trackers", value=len(asset_dirs))
col3_metric = col_cap3.metric(label="Terminal Refresh Cycle", value=f"#{st.session_state.run_count}")

st.markdown("<br>", unsafe_allow_html=True)

st.header("🗂️ Asset-by-Asset Realised Performance Allocation")
breakdown_cols = st.columns(len(asset_pnl_breakdown) if len(asset_pnl_breakdown) > 0 else 1)

for idx, (asset, pnl) in enumerate(asset_pnl_breakdown.items()):
    with breakdown_cols[idx]:
        st.markdown(f"""
        <div class='pnl-card'>
            <span class='cfd-name'>🔥 {asset}</span>
            <span style='font-size: 46px; font-weight:900; color: {"#00ffcc" if pnl >= 0 else "#ff4d4d"};'>${pnl:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.header("📈 Real-Time Ticket Execution & Transaction Stream Ledger")

if all_history and len(all_history) > 0:
    combined_df = pd.concat(all_history).sort_values(by="timestamp", ascending=False)
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
    combined_df.columns = [c.upper() for c in combined_df.columns]
    st.dataframe(combined_df, use_container_width=True, hide_index=True)
else:
    st.info("Awaiting structural indicator breakthroughs... No executions registered on this session ledger.")

st.components.v1.html(
    \"\"\"
    <script>
    setTimeout(function(){
        window.parent.location.reload();
    }, 60000);
    </script>
    \"\"\",
    height=0
)
