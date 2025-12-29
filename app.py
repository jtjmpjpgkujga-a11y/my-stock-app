import streamlit as st
import yfinance as yf
import pandas as pd
import time

# ページ設定
st.set_page_config(page_title="2026 財務戦略ボード", layout="wide")

st.title("📈 2026年戦略：財務推移・分析ボード")
st.caption("直近数年間の決算データを基に、企業の稼ぐ力を可視化します。")

# --- サイドバー設定 ---
st.sidebar.header("分析設定")
target_ticker = st.sidebar.text_input("銘柄コード (日本株は末尾に.T)", value="9984.T")

# 2026年戦略で重要な指標をセレクトボックスに
metric_options = {
    "ROE(%)": "自己資本利益率。資本効率の最重要指標です。",
    "ROA(%)": "総資産利益率。資産全体の稼ぐ力です。",
    "自己資本比率(%)": "財務の健全性を示します。",
    "EPS(1株利益)": "株価の源泉となる1株あたりの利益です。",
    "売上高(百万円)": "事業規模の成長性を確認します。",
    "純利益(百万円)": "最終的な儲けの推移です。"
}
selected_metric = st.sidebar.selectbox("表示する指標", list(metric_options.keys()))
st.sidebar.info(metric_options[selected_metric])

# --- メイン処理 ---
if st.button('データを取得して分析実行'):
    with st.spinner('Yahoo Financeから決算データを取得中...'):
        try:
            # データの取得
            stock
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="2026 銘柄分析ダッシュボード", layout="wide")
st.title("📈 銘柄深掘り分析：10年間の推移")

# サイドバー設定
st.sidebar.header("分析設定")
target_ticker = st.sidebar.text_input("分析したい銘柄コード (例: 9984.T)", value="9984.T")
period = st.sidebar.selectbox("期間", ["5y", "10y", "max"], index=1)
metric = st.sidebar.selectbox(
    "表示する指標", 
    ["ROE", "ROA", "自己資本比率", "純資産", "EPS(1株利益)"]
)

if st.button('分析を実行'):
    with st.spinner('過去の決算データを解析中...'):
        stock = yf.Ticker(target_ticker)
        
        # 1. 銘柄基本情報の表示
        info = stock.info
        st.subheader(f"🔍 {info.get('longName', target_ticker)} の詳細分析")
        
        # 2. 財務諸表（年次）の取得
        # financials: 損益計算書, balance_sheet: 貸借対照表
        fin = stock.financials.T
        bs = stock.balance_sheet.T
        
        if not fin.empty and not bs.empty:
            # 必要な指標の計算
            trend_df = pd.DataFrame(index=fin.index)
            
            # 指標の計算ロジック
            try:
                if metric == "ROE":
                    # ROE = 純利益 / 自己資本
                    trend_df["ROE(%)"] = (fin['Net Income'] / bs['Total Assets']) * 100 # 簡易的な分母
                elif metric == "ROA":
                    trend_df["ROA(%)"] = (fin['Net Income'] / bs['Total Assets']) * 100
                elif metric == "自己資本比率":
                    trend_df["自己資本比率(%)"] = (bs['Stockholders Equity'] / bs['Total Assets']) * 100
                elif metric == "純資産":
                    trend_df["純資産(百万円)"] = bs['Stockholders Equity'] / 1_000_000
                elif metric == "EPS(1株利益)":
                    trend_df["EPS"] = fin.get('Basic EPS', 0)
                
                # グラフ表示
                st.write(f"### {metric} の推移 ({period})")
                st.line_chart(trend_df)
                
                # 数値データ表示
                st.write("### 決算データ詳細")
                st.dataframe(trend_df.sort_index(ascending=False))
                
            except Exception as e:
                st.error(f"指標の計算中にエラーが発生しました: {e}")
                st.info("Yahoo Financeのデータ構造により、一部の古いデータが取得できない場合があります。")
        else:
            st.error("財務諸表データが見つかりませんでした。")

else:
    st.info("左のサイドバーから銘柄コードを入力し、表示したい指標を選んで「分析を実行」を押してください。")

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
