from fear_and_greed_parser import FearAndGreed
from yfinance_parser.market_index import MarketIndex, SpyTrailingIndex
from yfinance_parser.fred_index import VTICombinedIndex, FredIndex


def generate_dummy_data():
    """각 섹션 별로 요구된 데이터 구조에 맞게 생성"""
    nasdaq = MarketIndex(ticker="^IXIC", diff_year="20y")
    snp = MarketIndex(ticker="^GSPC", diff_year="20y")
    nasdaq_rsi = MarketIndex(ticker="^IXIC", diff_year="1y")
    snp_rsi = MarketIndex(ticker="^GSPC", diff_year="1y")
    fear_and_greed = FearAndGreed(diff_year=3)
    overvalued = VTICombinedIndex(ticker="VTI", diff_year="20y")
    spy_overvalued = SpyTrailingIndex(ticker="SPY", diff_year="20y")
    gold = MarketIndex(ticker="IAU", diff_year="20y")
    dollar = MarketIndex(ticker="DX-Y.NYB", diff_year="20y")
    cpi = FredIndex(ticker="CPIAUCSL", diff_year=20)
    gs2 = FredIndex(ticker="GS2", diff_year=20)
    gs10 = FredIndex(ticker="GS10", diff_year=20)
    sections = [
        {
            "text": "📌 1. 기본 지수 📌" + " || " + "나스닥 MDD:" + nasdaq.get_current_mdd() + " || " + "S&P MDD:" + snp.get_current_mdd(),
            "graphs": [
                {"id": "graph-1-1", "data": nasdaq.get_multiple_data(data_columns=["Close", "MA_200"],
                                                                     legend_labels=["Nasdaq Index", "200일 이평선"])},
                {"id": "graph-1-2", "data": snp.get_multiple_data(data_columns=["Close", "MA_200"],
                                                                  legend_labels=["S&P Index", "200일 이평선"])},
                {"id": "graph-1-3", "data": nasdaq_rsi.get_data(data_column="RSI",
                                                                legend_label="Nasdaq RSI")},
                {"id": "graph-1-4", "data": snp_rsi.get_data(data_column="RSI",
                                                             legend_label="S&P RSI")},
                {"id": "graph-1-5", "data": nasdaq.get_data(data_column="MDD",
                                                            legend_label="Nasdaq 하락폭")},
                {"id": "graph-1-6", "data": snp.get_data(data_column="MDD",
                                                         legend_label="S&P 하락폭")},
            ]
        },
        {
            "text": "📣 2. 공포 지수 📣" + " || " + fear_and_greed.get_current_status(),
            "graphs": [
                {"id": "graph-2-1", "data": fear_and_greed.get_data(data_column="fear_and_greed_historical",
                                                                    legend_label="fear and greed")},
                {"id": "graph-2-2", "data": fear_and_greed.get_data(data_column="safe_haven_demand",
                                                                    legend_label="채권 선호도(안전 자산 선호도)")},
                {"id": "graph-2-3", "data": fear_and_greed.get_data(data_column="put_call_options",
                                                                    legend_label="풋 콜 옵션(숏 비중)")},
            ]
        },
        {
            "text": "📈 3. 고평가 지표 📈",
            "graphs": [
                {"id": "graph-3-1", "data": overvalued.get_buffett_data(data_column="buffett_index",
                                                                        legend_label="버핏 지수")},
                {"id": "graph-3-2", "data": overvalued.get_m2_per_marketcap(data_column="m2_per_marketcap",
                                                                            legend_label="유동성 대비 주식 지수(M2 / 시총)")},
                {"id": "graph-3-3", "data": spy_overvalued.get_data(data_column="pe_ratio",
                                                                    legend_label="S&P P/E (SPY 추정치)")},
                # {"id": "graph-3-4", "datasets": 5, "legend_label": "Magnificent 7 MDD"}
            ]
        },
        {
            "text": "🌍 4. 기타 거시경제 지표 🌍",
            "graphs": [
                {"id": "graph-4-1", "data": dollar.get_multiple_data(data_columns=["Close", "MA_200"],
                                                                     legend_labels=["달러 인덱스", "200일 이평선"])},
                {"id": "graph-4-2", "data": gold.get_multiple_data(data_columns=["Close", "MA_200"],
                                                                   legend_labels=["금 ETF 가격", "200일 이평선"])},
                {"id": "graph-4-3", "data": cpi.get_data(data_column="Normed", legend_label="미국 CPI")},
                {"id": "graph-4-4", "data": (gs2.get_data(data_column="GS2", legend_label="미국 2년 단기채 금리") +
                                             gs10.get_data(data_column="GS10", legend_label="미국 10년 장기채 금리"))}
            ]
        }
    ]

    return {"sections": sections}
