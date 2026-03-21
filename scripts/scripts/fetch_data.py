#!/usr/bin/env python3
"""
投資学習ダッシュボード — 株価データ自動取得スクリプト
yfinance を使って全銘柄の最新データを取得し data.json に保存する。
GitHub Actions から毎日1回実行される想定。
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

# ── ティッカー変換マップ ──────────────────────────────
# index.html 内のティッカー → yfinance 用ティッカー
TICKER_MAP = {
    # 日本株は .T を付ける
    "7203": "7203.T", "7974": "7974.T", "6920": "6920.T",
    "8058": "8058.T", "7011": "7011.T", "7012": "7012.T",
    "5631": "5631.T", "6701": "6701.T", "7013": "7013.T",
    "3692": "3692.T", "4258": "4258.T", "3927": "3927.T",
    "4493": "4493.T", "4417": "4417.T",
    "7711": "7711.T", "4026": "4026.T", "6965": "6965.T",
    "5310": "5310.T", "3446": "3446.T",
    "6269": "6269.T", "6350": "6350.T", "7003": "7003.T",
    "6326": "6326.T", "6310": "6310.T", "4997": "4997.T", "6316": "6316.T",
    "3687": "3687.T", "6864": "6864.T", "6728": "6728.T", "6807": "6807.T",
    "186A": "186A.T", "5595": "5595.T", "290A": "290A.T",
    "9412": "9412.T", "9348": "9348.T",
    "8802": "8802.T", "8801": "8801.T", "8830": "8830.T",
    "1812": "1812.T", "1801": "1801.T",
    "3360": "3360.T", "2374": "2374.T", "160A": "160A.T",
    "9158": "9158.T", "286A": "286A.T",
    "6189": "6189.T", "7358": "7358.T", "2749": "2749.T",
    "2462": "2462.T", "9215": "9215.T",
    "9041": "9041.T", "9042": "9042.T", "9503": "9503.T",
    "9532": "9532.T", "1802": "1802.T",
    "8035": "8035.T", "6146": "6146.T", "7735": "7735.T",
    "6301": "6301.T",
    # 韓国株
    "005930": "005930.KS",
    "000660": "000660.KS",
    # 香港株
    "0700": "0700.HK",
    # 中国株 (BYD - 香港上場)
    "1211": "1211.HK",
    # 欧州株
    "NOVO-B": "NOVO-B.CO",   # Novo Nordisk (コペンハーゲン)
    "VOW3": "VOW3.DE",       # Volkswagen (フランクフルト)
    "SIE": "SIE.DE",         # Siemens
    "MAERSK": "MAERSK-B.CO", # Maersk (コペンハーゲン)
    "BA.L": "BA.L",          # BAE Systems (ロンドン)
    "DG.PA": "DG.PA",        # Vinci (パリ)
    "FER.MC": "FER.MC",      # Ferrovial (マドリード)
    "VIE.PA": "VIE.PA",      # Veolia (パリ)
    "TTE": "TTE",            # TotalEnergies (NYSE上場)
    # その他はそのまま（米国株）
}


def get_yf_ticker(ticker: str) -> str:
    """index.html のティッカーを yfinance 用に変換"""
    return TICKER_MAP.get(ticker, ticker)


def extract_all_tickers(html_path: str) -> list[str]:
    """index.html から全ティッカーを抽出"""
    import re
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # S("TICKER", ...) パターンにマッチ
    pattern = r'S\("([^"]+)",'
    tickers = re.findall(pattern, html)
    # 重複除去 (順序保持)
    seen = set()
    unique = []
    for t in tickers:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def fetch_stock_data(tickers: list[str]) -> dict:
    """yfinance で全銘柄のデータを一括取得（10年分の週次履歴含む）"""
    yf_tickers = [get_yf_ticker(t) for t in tickers]
    ticker_to_original = {get_yf_ticker(t): t for t in tickers}

    print(f"Fetching data for {len(yf_tickers)} tickers...")

    # yfinance の一括ダウンロード (直近2日分の日足)
    data = yf.download(yf_tickers, period="2d", group_by="ticker", progress=False)

    # 10年分の履歴データを一括取得（週次に間引いてファイルサイズを抑制）
    print("Fetching 10-year history (weekly)...")
    hist_data = yf.download(yf_tickers, period="10y", interval="1wk", group_by="ticker", progress=False)

    # 個別銘柄の詳細情報を取得
    result = {}
    failed = []

    for yf_t, orig_t in ticker_to_original.items():
        try:
            stock = yf.Ticker(yf_t)
            info = stock.info

            # 株価
            price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
            if price is None:
                failed.append(orig_t)
                continue

            # 前日比変動率
            prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
            if prev_close and prev_close > 0:
                change = round(((price - prev_close) / prev_close) * 100, 2)
            else:
                change = 0.0

            # PER
            pe = info.get("trailingPE") or info.get("forwardPE")
            if pe:
                pe = round(pe, 1)
            else:
                pe = 0

            # 配当利回り (%)
            div_yield = info.get("dividendYield")
            if div_yield:
                div_yield = round(div_yield * 100, 2)
            else:
                div_yield = 0.0

            # 10年分の週次履歴データ
            history = []
            try:
                if len(yf_tickers) == 1:
                    hist_close = hist_data["Close"]
                else:
                    hist_close = hist_data[yf_t]["Close"] if yf_t in hist_data.columns.get_level_values(0) else None

                if hist_close is not None:
                    for date, val in hist_close.dropna().items():
                        history.append({
                            "date": f"{date.year}/{date.month}",
                            "p": round(float(val), 2)
                        })
            except Exception:
                pass  # 履歴取得失敗時はスキップ

            entry = {
                "price": round(price, 2),
                "change": change,
                "pe": pe,
                "div": div_yield,
            }
            if history:
                entry["history"] = history

            result[orig_t] = entry

            hist_info = f" [{len(history)}pts]" if history else ""
            print(f"  ✓ {orig_t} → ¥{price} ({change:+.2f}%){hist_info}")

        except Exception as e:
            failed.append(orig_t)
            print(f"  ✗ {orig_t}: {e}")

    if failed:
        print(f"\n⚠ Failed to fetch {len(failed)} tickers: {', '.join(failed)}")

    return result


def main():
    # パス設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    html_path = os.path.join(root_dir, "index.html")
    output_path = os.path.join(root_dir, "data.json")

    # ティッカー抽出
    tickers = extract_all_tickers(html_path)
    print(f"Found {len(tickers)} tickers in index.html")

    # データ取得
    stock_data = fetch_stock_data(tickers)

    # JSON出力
    jst = timezone(timedelta(hours=9))
    output = {
        "updated_at": datetime.now(jst).strftime("%Y-%m-%d %H:%M JST"),
        "count": len(stock_data),
        "stocks": stock_data,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved {len(stock_data)} stocks to data.json")
    print(f"   Updated at: {output['updated_at']}")


if __name__ == "__main__":
    main()
