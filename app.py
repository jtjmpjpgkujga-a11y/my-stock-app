import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="2026 財務比較ボード", layout="wide")
st.title("🚀 ワンタッチ銘柄比較ダッシュボード")

# サイドバー設定
st.sidebar.header("設定")
default_tickers = "9984.T, 7203.T, 8058.T"
input_tickers = st.sidebar.text_area(
    "銘柄コードを入力（日本株は末尾に.T）", 
    value=default_tickers
)

ticker_list = [t.strip() for t in input_tickers.split(",") if t.strip()]

if st.button('データを取得して比較'):
    if not ticker_list:
        st.error("銘柄コードを入力してください")
    else:
        data = []
        with st.spinner('財務データを取得中...'):
            for ticker in ticker_list:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    
                    data.append({
                        "コード": ticker,
                        "銘柄名": info.get("shortName", ticker),
                        "PER": info.get("forwardPE"),
                        "PBR": info.get("priceToBook"),
                        "ROE(%)": (info.get("returnOnEquity", 0) or 0) * 100,
                        "ROA(%)": (info.get("returnOnAssets", 0) or 0) * 100,
                        "ROIC(%)": (info.get("operatingMargins", 0) * 0.7) * 100 if info.get("operatingMargins") else None,
                        "純資産(百万円)": int((info.get("totalStockholderEquity", 0) or 0) / 1_000_000),
                    })
                except Exception as e:
                    st.warning(f"{ticker} のデータ取得に失敗しました。")

        if data:
            df = pd.DataFrame(data)
            st.subheader("📋 財務指標リスト")
            # 数値のフォーマットを整える
            st.dataframe(
                df.set_index("コード").style.format({
                    "PER": "{:.2f}",
                    "PBR": "{:.2f}",
                    "ROE(%)": "{:.2f}",
                    "ROA(%)": "{:.2f}",
                    "ROIC(%)": "{:.2f}",
                    "純資産(百万円)": "{:,}"
                }), 
                use_container_width=True
            )

            # グラフ表示
            st.subheader("📊 純資産の比較（百万円）")
            st.bar_chart(df.set_index("銘柄名")["純資産(百万円)"])

            st.subheader("📈 収益性・効率性の比較")
            st.bar_chart(df.set_index("銘柄名")[["ROE(%)", "ROIC(%)"]])
else:
    st.info("左側のサイドバーに銘柄を入力し、ボタンを押してください。")
