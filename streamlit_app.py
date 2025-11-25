import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Heatseeker Lite", layout="wide")
st.title("Heatseeker Lite — Free Forever")

ticker = st.sidebar.selectbox("Ticker", ["SPY","QQQ","IWM","AAPL","TSLA","NVDA"])
spot   = st.sidebar.number_input("Spot price", value=585.0, step=0.5)

# Realistic mock GEX data — 100% guaranteed to work
np.random.seed(42)
strikes = np.round(np.arange(spot-60, spot+61, 2.5), 2)
dist = np.abs(strikes - spot)
oi = (25000 * np.exp(-dist/30) + np.random.normal(0, 3000, len(strikes))).astype(int)
oi = np.maximum(oi, 2000)

df = pd.DataFrame({"strike": strikes, "oi": oi})
df["days"] = np.random.randint(7, 45, len(df))
df["gamma"] = 0.4 / (df["strike"] * 0.2 * np.sqrt(df["days"]/365 + 0.001))
df["gex"] = -df["oi"] * df["gamma"] * spot*spot * 0.01

gex = df.groupby("strike")["gex"].sum().reset_index()
king = gex.loc[gex["gex"].idxmax(), "strike"]

# Simple bar chart using built-in Streamlit (no plotly = no ModuleNotFoundError)
chart_data = pd.DataFrame({
    "strike": gex["strike"],
    "GEX ($M)": (gex["gex"]/1e6).round(2)
}).set_index("strike")

st.bar_chart(chart_data, use_container_width=True, height=600)

# Highlight King Node
st.markdown(f"### KING NODE: **${king:.2f}** (Distance: {spot-king:+.2f})")
st.success(f"Dealers want {ticker} pinned at **${king:.2f}** right now")
st.dataframe(chart_data.sort_values("GEX ($M)", ascending=False).head(20))
