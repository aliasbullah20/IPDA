import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="IPDA BOSKU", layout="wide")
st.title("IPDA SCREENER - Punya Bosku")
st.caption("Filter Vol/MCap > 20% | Data CoinGecko")

min_ratio = st.slider("Minimal Vol/MCap (%)", 5, 100, 20)

@st.cache_data(ttl=300)
def ambil_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=volume_desc&per_page=250&page=1&sparkline=false&price_change_percentage=24h,7d,30d"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df['vol_mcap'] = (df['total_volume'] / df['market_cap'] * 100).round(2)
    return df

try:
    df = ambil_data()
    lolos = df[df['vol_mcap'] >= min_ratio].sort_values('vol_mcap', ascending=False)
    st.success(f"Ada {len(lolos)} koin lolos filter {min_ratio}%")
    st.dataframe(lolos[['name','symbol','current_price','vol_mcap','total_volume','market_cap']], use_container_width=True)
except Exception as e:
    st.error(f"Gagal: {e}")
