import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="2026 財務比較ボード", layout="wide")
st.title("🚀 ワンタッチ銘柄比較ダッシュボード")

# サイドバー設定
st.sidebar.header("設定")
default_tickers = "9984.T, 7203.T, 8058.T"
input_tickers = st.sidebar.text_area(
    "銘柄コードを入力（カンマ区切り、日本株は末尾に.T）", 
    value=default_tickers
)

ticker_list = [t.strip() for t in input_tickers.split(",") if t.strip()]

if st.button('データを取得して比較'):
    if not ticker_list:
        st.error("銘柄コードを入力してください")
    else:
        data = []
        progress_bar = st.progress(0)
        
        for i, ticker in enumerate(ticker_list):
            try:
                # 取得の安定性を高めるため、少し待機（連続アクセス対策）
                time.sleep(0.5)
                stock = yf.Ticker(ticker)
                # fast_infoを使って基本データを優先取得
                info = stock.info
                
                # 安全に値を取得するための補助関数
                def get_val(key):
                    return info.get(key) if info.get(key) is not None else 0

                data.append({
                    "コード": ticker,
                    "銘柄名": info.get("shortName") or info.get("longName") or ticker,
                    "PER": info.get("forwardPE") or info.get("trailingPE"),
                    "PBR": info.get("priceToBook"),
                    "ROE(%)": get_val("returnOnEquity") * 100,
                    "ROA(%)": get_val("returnOnAssets") * 100,
                    "ROIC(%)": (get_val("operatingMargins") * 0.7) * 100,
                    "純資産(百万円)": int(get_val("totalStockholderEquity") / 1_000_000),
                })
            except Exception as e:
                st.warning(f"{ticker}: 通信エラーまたはデータ未登録です。")
            
            progress_bar.progress((i + 1) / len(ticker_list))

        if data:
            df = pd.DataFrame(data)
            st.subheader("📋 財務指標リスト")
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

            st.subheader("📊 純資産の比較（百万円）")
            st.bar_chart(df.set_index("銘柄名")["純資産(百万円)"])
        else:
            st.error("表示できるデータがありませんでした。コードが正しいか（例：9984.T）確認してください。")
