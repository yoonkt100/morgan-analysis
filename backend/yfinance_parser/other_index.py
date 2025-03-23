import yfinance as yf
import pandas as pd


class IndividualIndex:
    def __init__(self, ticker, diff_year):
        self.ticker = ticker
        self.diff_year = diff_year
        self.df = self._get_market_index_data()

    def _get_market_index_data(self):
        market = yf.Ticker(self.ticker)
        market_hist = market.history(period=self.diff_year)
        market_hist = market_hist.reset_index()
        market_hist.rename(columns={'Date': 'date'}, inplace=True)
        close = market_hist['Close']

        # 200일 이평선 계산
        market_hist['MA_200'] = market_hist['Close'].rolling(window=200).mean()

        # RSI 계산 (14일 기준)
        market_hist['RSI'] = compute_rsi(close)

        # MDD 계산
        cum_max = close.cummax()
        drawdown = (close - cum_max) / cum_max
        market_hist['MDD'] = drawdown

        return market_hist

    def get_data(self, data_column, legend_label):
        datasets = [{
            "data": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(self.df["date"]).tolist()],
            "labels": self.df[data_column].tolist(),
            "legend_label": legend_label
        }]
        return datasets

    def get_multiple_data(self, data_columns, legend_labels):
        datasets = []
        for data_column, legend_label in zip(data_columns, legend_labels):
            datasets.append({
                "data": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(self.df["date"]).tolist()],
                "labels": self.df[data_column].tolist(),
                "legend_label": legend_label
            })
        return datasets
