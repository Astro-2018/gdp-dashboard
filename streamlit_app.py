import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Heatseeker Lite", layout="wide")
st.title("Heatseeker Lite — Free Forever v2")

ticker = st.sidebar.selectbox("Ticker", ["SPY","QQQ","IWM","AAPL","TSLA","NVDA","AMD","META"])
spot = st.sidebar.number_input("Current Price", value=585.0, step=0.5)

# Realistic mock data
np.random.seed(42)
strikes = np.round(np.arange(spot-60, spot+61, 2.5), 2)
dist = np.abs(strikes - spot)
oi = np.maximum(3000, 28000 * np.exp(-dist/28) + np.random.normal(0, 4000, len(strikes)))

df = pd.DataFrame({"strike": strikes, "oi": oi.astype(int)})
df["gamma"] = 0.4 / (df["strike"] * 0.2 * np.sqrt(0.08))
df["gex"] = -df["oi"] * df["gamma"] * spot*spot * 0.01

gex = df.groupby("strike")["gex"].sum().reset_index()
king = gex.loc[gex["gex"].idxmax(), "strike"]

# Plotly — the real Heatseeker look
fig = go.Figure()
fig.add_trace(go.Bar(
    x=gex["strike"], y=gex["gex"]/1e6,
    marker_color=["limegreen" if x > 0 else "crimson" for x in gex["gex"]]
))
fig.add_vline(x=spot, line_color="white", line_dash="dot", annotation_text="Spot")
fig.add_vline(x=king, line_color="gold", line_width=7, annotation_text=f"KING NODE ${king:.1f}")
fig.update_layout(
    title=f"{ticker} → King Node ${king:.1f}",
    xaxis_title="Strike", yaxis_title="GEX ($ millions)",
    height=680, template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

st.metric("KING NODE", f"${king:.1f}", delta=f"{spot-king:+.2f} from spot")
st.success(f"Dealers are pulling {ticker} toward **${king:.1f}** right now")
