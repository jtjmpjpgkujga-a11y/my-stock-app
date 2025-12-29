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
            stock = yf.Ticker(target_ticker)
            info = stock.info
            fin = stock.financials.T      # 損益計算書
            bs = stock.balance_sheet.T    # 貸借対照表
            
            if fin.empty or bs.empty:
                st.error("財務データが見つかりませんでした。コード（.Tなど）を確認してください。")
            else:
                # データの整理
                df = pd.DataFrame(index=fin.index)
                
                # 指標の計算
                if selected_metric == "ROE(%)":
                    df[selected_metric] = (fin['Net Income'] / bs['Stockholders Equity']) * 100
                elif selected_metric == "ROA(%)":
                    df[selected_metric] = (fin['Net Income'] / bs['Total Assets']) * 100
                elif selected_metric == "自己資本比率(%)":
                    df[selected_metric] = (bs['Stockholders Equity'] / bs['Total Assets']) * 100
                elif selected_metric == "EPS(1株利益)":
                    df[selected_metric] = fin.get('Basic EPS', 0)
                elif selected_metric == "売上高(百万円)":
                    df[selected_metric] = fin['Total Revenue'] / 1_000_000
                elif selected_metric == "純利益(百万円)":
                    df[selected_metric] = fin['Net Income'] / 1_000_000

                # --- 画面表示 ---
                st.subheader(f"🔍 {info.get('shortName', target_ticker)} の {selected_metric} 推移")
                
                # 折れ線グラフ
                st.line_chart(df[selected_metric])
                
                # データテーブル
                st.write("### 決算詳細数値")
                st.dataframe(
                    df.sort_index(ascending=False).style.format("{:,.2f}"),
                    use_container_width=True
                )
                
                # おまけ：現在の株価情報
                col1, col2, col3 = st.columns(3)
                col1.metric("現在値", f"{info.get('currentPrice')} {info.get('currency')}")
                col2.metric("PER", f"{info.get('forwardPE', 'N/A')}")
                col3.metric("PBR", f"{info.get('priceToBook', 'N/A')}")

        except Exception as e:
            st.error(f"データ処理中にエラーが発生しました。")
            st.info(f"ヒント: 日本株の場合、一部の指標が公開されていない場合があります。")
else:
    st.info("左側のサイドバーに銘柄コードを入れて「分析実行」を押してください。")
