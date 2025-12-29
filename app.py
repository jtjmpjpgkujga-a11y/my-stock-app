import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="2026銘柄戦略ボード", layout="wide")

st.title("📈 2026年戦略：銘柄比較ボード")

# 保存された銘柄リストと戦略メモ
# ※ここを書き換えればいつでもリストを更新できます
my_stocks = {
    "9984.T": "ソフトバンクG：AI戦略の核として注目",
    "7203.T": "トヨタ：EV・水素戦略の進捗を確認",
    "8058.T": "三菱商事：累進配当と株主還元を評価"
}

if st.button('データを更新する'):
    data = []
    with st.spinner('最新データを取得中...'):
        for ticker, memo in my_stocks.items():
            stock = yf.Ticker(ticker)
            info = stock.info
            data.append({
                "銘柄名": info.get("longName", ticker),
                "現在値": info.get("currentPrice"),
                "PER": info.get("forwardPE"),
                "利回り(%)": (info.get("dividendYield", 0) or 0) * 100,
                "自己資本比率": info.get("debtToEquity"),
                "戦略メモ": memo
            })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    # 視覚的比較：利回りのグラフ
    st.subheader("配当利回り比較")
    st.bar_chart(df.set_index("銘柄名")["利回り(%)"])
else:
    st.write("上のボタンを押すと、最新の財務データを取得します。")
