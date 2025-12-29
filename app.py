import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="2026戦略・銘柄分析", layout="wide")

st.title("📊 銘柄比較ダッシュボード")

# スクリーンショットに基づいた銘柄リスト
my_stocks = {
    "9744.T": "メイテックグループ",
    "9682.T": "ＤＴＳ",
    "7803.T": "ブシロード",
    "3844.T": "コムチュア",
    "3692.T": "ＦＦＲＩセキュリティ",
    "3635.T": "コーエーテクモＨＤ",
    "8593.T": "三菱ＨＣキャピタル",
    "9508.T": "九州電力",
    "3387.T": "クリエイト・レストランツ",
    "7970.T": "信越ポリマー",
    "2670.T": "エービーシー・マート"
}

if st.button('最新データを取得・分析'):
    data = []
    with st.spinner('財務データを計算中...'):
        for ticker, name in my_stocks.items():
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 貸借対照表などの詳細データを取得
            fin = stock.financials
            bs = stock.balance_sheet
            
            # 各指標の計算と取得
            try:
                # ROICの簡易計算: 営業利益 / (自己資本 + 有利子負債)
                ebit = info.get("operatingCashflow", 0) # 簡易的にCFを使用
                total_equity = info.get("totalStockholderEquity", 1)
                total_debt = info.get("totalDebt", 0)
                roic = (info.get("operatingEarnings", 0) / (total_equity + total_debt)) * 100 if (total_equity + total_debt) > 0 else 0
                
                data.append({
                    "銘柄名": name,
                    "コード": ticker,
                    "PER": info.get("forwardPE"),
                    "PBR": info.get("priceToBook"),
                    "ROE(%)": (info.get("returnOnEquity", 0) or 0) * 100,
                    "ROA(%)": (info.get("returnOnAssets", 0) or 0) * 100,
                    "ROIC(%)": roic,
                    "純資産(億円)": (info.get("totalStockholderEquity", 0) or 0) / 100000000
                })
            except:
                continue

    df = pd.DataFrame(data)

    # 1. 指標リスト（表）の表示
    st.subheader("📋 財務指標一覧")
    st.dataframe(df.style.highlight_max(axis=0, color='#112233'), use_container_width=True)

    # 2. 縦軸グラフ（各指標の比較）
    st.subheader("📊 指標別 比較グラフ")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("▼ PER・PBR比較")
        st.bar_chart(df.set_index("銘柄名")[["PER", "PBR"]])
        
        st.write("▼ 純資産（億円）")
        st.bar_chart(df.set_index("銘柄名")["純資産(億円)"])

    with col2:
        st.write("▼ 収益性（ROE / ROA / ROIC）")
        st.bar_chart(df.set_index("銘柄名")[["ROE(%)", "ROA(%)", "ROIC(%)"]])

else:
    st.info("「最新データを取得・分析」ボタンを押すと、グラフとリストが表示されます。")
