import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from prophet import Prophet
from datetime import datetime
import urllib3

# ===== CONFIGURAÇÃO =====
st.set_page_config(page_title="CryptoMind Dashboard", page_icon="💸", layout="wide")
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
[data-testid="stMetricValue"] {font-size: 24px;}
[data-testid="stMetricLabel"] {font-size: 16px;}
</style>
""", unsafe_allow_html=True)

st.title("💸 CryptoMind Dashboard")
st.caption("Preços atuais e previsão das maiores criptomoedas 📈")

# ===== OPÇÕES =====
selected_currency = st.sidebar.selectbox("💱 Moeda base", ["usd", "eur", "brl"])
refresh_time = st.sidebar.slider("⏱️ Atualizar a cada (segundos)", 60, 600, 120)

# ===== FUNÇÃO PARA PEGAR DADOS =====
@st.cache_data(ttl=refresh_time)
def get_crypto_data(vs_currency="usd"):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": True
    }
    try:
        response = requests.get(url, params=params, verify=False, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
        return pd.DataFrame()

# ===== PLACEHOLDER =====
placeholder = st.empty()
df = get_crypto_data(selected_currency)

if not df.empty:
    with placeholder.container():
        # ===== MÉTRICAS =====
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Preço médio", f"{df['current_price'].mean():,.2f} {selected_currency.upper()}")
        col2.metric("📈 Maior preço", f"{df['current_price'].max():,.2f} {selected_currency.upper()}")
        col3.metric("📉 Menor preço", f"{df['current_price'].min():,.2f} {selected_currency.upper()}")

        # ===== GRÁFICO DE PREÇO + PREVISÃO =====
        fig = go.Figure()
        for _, row in df.iterrows():
            # Histórico seguro
            prices = row['sparkline_in_7d']['price'] if 'sparkline_in_7d' in row and 'price' in row['sparkline_in_7d'] else [row['current_price']] * 7
            history = pd.DataFrame({
                'ds': pd.date_range(end=datetime.today(), periods=len(prices)),
                'y': prices
            })

            # Treina Prophet apenas uma vez por carga
            model = Prophet(daily_seasonality=True)
            model.fit(history)
            future = model.make_future_dataframe(periods=3)
            forecast = model.predict(future)

            # Linha preço atual
            fig.add_trace(go.Scatter(
                x=history['ds'],
                y=history['y'],
                mode='lines+markers',
                name=f"{row['symbol']} - Atual"
            ))

            # Linha previsão
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat'],
                mode='lines',
                name=f"{row['symbol']} - Previsão",
                line=dict(dash='dot')
            ))

        fig.update_layout(
            title=f"💹 Preço Atual + Previsão ({selected_currency.upper()})",
            template="plotly_dark",
            xaxis_title="Data",
            yaxis_title=f"Preço ({selected_currency.upper()})",
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ===== TABELA DETALHADA =====
        st.subheader("📊 Dados Detalhados")
        st.dataframe(df[["id","symbol","current_price","high_24h","low_24h","price_change_percentage_24h"]])

        st.caption(f"🔄 Última atualização: {datetime.now().strftime('%H:%M:%S')}")

else:
    st.warning("Nenhum dado disponível 😕")


