import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="2026 財務比較ボード", layout="wide")
st.title("🚀 ワンタッチ銘柄比較ダッシュボード")

# サイドバーで銘柄を入力・選択できるようにする
st.sidebar.header("設定")
default_tickers = "9984.T, 7203.T, 8058.T"
input_tickers = st.sidebar.text_area(
    "銘柄コードを入力（カンマ区切り、日本株は末尾に.T）", 
    value=default_tickers,
    help="例: 9984.T, 7203.T, AAPL"
)

# 入力された文字列をリストに変換
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
                    
                    # データの抽出
                    data.append({
                        "コード": ticker,
                        "銘柄名": info.get("longName", ticker),
                        "PER": info.get("forwardPE"),
                        "PBR": info.get("priceToBook"),
                        "ROE(%)": (info.get("returnOnEquity", 0) or 0) * 100,
                        "ROA(%)": (info.get("returnOnAssets", 0) or 0) * 100,
                        # ROICは簡易的に (営業利益 * (1-税率)) / (有利子負債 + 自己資本) で計算
                        "ROIC(%)": (info.get("operatingMargins", 0) * 0.7) * 100 if info.get("operatingMargins") else None,
                        "純資産(兆円)": (info.get("totalStockholderEquity", 0) or 0) / 1e12,
                    })
                except Exception as e:
                    st.warning(f"{ticker} のデータ取得に失敗しました。")

        if data:
            df = pd.DataFrame(data)

            # リスト表示
            st.subheader("📋 財務指標リスト")
            st.dataframe(df.set_index("コード"), use_container_width=True)

            # グラフ表示
            st.subheader("📊 資本効率の比較（ROE vs ROIC）")
            st.bar_chart(df.set_index("銘柄名")[["ROE(%)", "ROIC(%)"]])

            st.subheader("📉 割安性の比較（PER / PBR）")
            col1, col2 = st.columns(2)
            with col1:
                st.write("PER")
                st.bar_chart(df.set_index("銘柄名")["PER"])
            with col2:
                st.write("PBR")
                st.bar_chart(df.set_index("銘柄名")["PBR"])
        else:
            st.error("有効な銘柄データが見つかりませんでした。")
else:
    st.info("左側のサイドバーに銘柄を入力し、ボタンを押してください。")
