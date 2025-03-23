import yfinance as yf
import pandas as pd

from utils import compute_rsi


class MarketIndex:
    def __init__(self, ticker, diff_year):
        self.ticker = ticker
        self.diff_year = diff_year  # 2008 부터 보려면 20
        self.df = self._get_market_index_data()

    def _get_market_index_data(self):
        market = yf.Ticker(self.ticker)
        market_hist = market.history(period=self.diff_year)
        market_hist = market_hist.reset_index()
        market_hist.rename(columns={'Date': 'date'}, inplace=True)
        close = market_hist['Close']

        # 200일 이평선 계산
        market_hist['MA_200'] = market_hist['Close'].rolling(window=200).mean().fillna(0)

        # RSI 계산 (14일 기준)
        market_hist['RSI'] = compute_rsi(close).fillna(0)

        # MDD 계산
        cum_max = close.cummax()
        drawdown = (close - cum_max) / cum_max
        market_hist['MDD'] = drawdown

        # 정규화 (처음 값을 100으로)
        close_base = market_hist['Close'].iloc[0]
        market_hist['Normed'] = market_hist['Close'] / close_base * 100

        return market_hist

    def get_current_mdd(self):
        mdd = self.df['MDD'].iloc[-1]
        return f"( 📉 {mdd:.3f} )"

    def get_data(self, data_column, legend_label):
        datasets = [{
            "data": self.df[data_column].tolist(),
            "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(self.df["date"]).tolist()],
            "legend_label": legend_label
        }]
        return datasets

    def get_multiple_data(self, data_columns, legend_labels):
        datasets = []
        for data_column, legend_label in zip(data_columns, legend_labels):
            datasets.append({
                "data": self.df[data_column].tolist(),
                "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(self.df["date"]).tolist()],
                "legend_label": legend_label
            })
        return datasets


class SpyTrailingIndex:
    def __init__(self, ticker, diff_year):
        self.ticker = ticker  # SPY
        self.diff_year = diff_year  # 2008 부터 보려면 20
        self.df = self._get_spy_data()

    def _get_spy_data(self):
        # 1. SPY 정보 불러오기
        spy = yf.Ticker(self.ticker)
        info = spy.info

        # 2. 현재 가격과 trailing PER 가져오기
        price = info.get('previousClose')
        pe = info.get('trailingPE')

        # 3. EPS 추정
        eps = price / pe

        # 4. SPY 가격 데이터 (20년치)
        price_df = spy.history(period=self.diff_year)
        price_df = price_df[['Close']].rename(columns={'Close': 'spy_price'})
        price_df = price_df.reset_index()
        price_df.rename(columns={'Date': 'date'}, inplace=True)

        # 5. P/E Ratio 계산
        price_df['pe_ratio'] = price_df['spy_price'] / eps
        return price_df

    def get_data(self, data_column, legend_label):
        datasets = [{
            "data": self.df[data_column].tolist(),
            "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(self.df["date"]).tolist()],
            "legend_label": legend_label
        }]
        return datasets
