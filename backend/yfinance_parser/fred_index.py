import datetime

import yfinance as yf
import pandas as pd
import pandas_datareader.data as web


class VTICombinedIndex:
    def __init__(self, ticker, diff_year):
        self.ticker = ticker  # VTI
        self.diff_year = diff_year  # 2008 부터 보려면 20
        self.end_date = datetime.datetime.today()
        self.start_date = self.end_date - datetime.timedelta(days=365 * int(diff_year[:2]))

    def get_buffett_data(self, data_column, legend_label):
        # 1. GDP 데이터 (분기별, 단위: Billion USD)
        gdp = web.DataReader('GDP', 'fred', self.start_date, self.end_date)
        gdp.index.name = 'date'
        gdp['gdp'] = gdp['GDP'] * 1_000_000_000  # → 달러 단위로 변환
        gdp['quarter'] = gdp.index.to_period('Q').astype(str)
        gdp = gdp.reset_index()
        gdp.rename(columns={'date': 'date'}, inplace=True)

        # 2. VTI 정보 불러오기
        vti = yf.Ticker(self.ticker)
        vti_hist = vti.history(period=self.diff_year)
        vti_hist = vti_hist.resample('QE').last()  # 분기별 종가
        vti_hist = vti_hist[['Close']].rename(columns={'Close': 'vti_price'})
        vti_hist.index.name = 'date'
        vti_hist.index = vti_hist.index.tz_localize(None)
        vti_hist['quarter'] = vti_hist.index.to_period('Q').astype(str)
        vti_hist = vti_hist.reset_index()
        vti_hist.rename(columns={'date': 'date'}, inplace=True)

        # 3. 시가총액 추정: 최신 시가총액 기반 비례계산
        latest_market_cap = vti.info['marketCap']
        latest_price = vti.info['previousClose']
        shares_outstanding = latest_market_cap / latest_price

        # 각 분기의 시가총액 추정
        vti_hist['vti_market_cap'] = vti_hist['vti_price'] * shares_outstanding

        # 4. 버핏 지수 계산
        merged = pd.merge(vti_hist, gdp, on='quarter', how='left')
        merged['buffett_index'] = (merged['vti_market_cap'] / merged['gdp']) * 10000
        merged.dropna(inplace=True)

        # Dataset 반환
        datasets = [{
            "data": merged[data_column].tolist(),
            "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(merged["date_x"]).tolist()],
            "legend_label": legend_label
        }]
        return datasets

    def get_m2_per_marketcap(self, data_column, legend_label):
        # 1. M2 데이터 (월간, billions of USD)
        m2 = web.DataReader('M2SL', 'fred', self.start_date, self.end_date)
        m2.index.name = 'date'
        m2['m2'] = m2['M2SL'] * 1e9  # 달러 단위
        m2 = m2.reset_index()
        m2.rename(columns={'date': 'date'}, inplace=True)

        # 2. VTI 가격 (yfinance, 월말 종가)
        vti = yf.Ticker(self.ticker)
        vti_hist = vti.history(period=self.diff_year)
        vti_hist = vti_hist.resample('ME').last()  # 월별 종가
        vti_hist = vti_hist[['Close']].rename(columns={'Close': 'vti_price'})
        vti_hist.index = vti_hist.index + pd.Timedelta(days=1)  # 하루 더하기 (fred는 1일, vti는 31일 발표)
        vti_hist.index.name = 'date'
        vti_hist.index = vti_hist.index.tz_localize(None)
        vti_hist = vti_hist.reset_index()
        vti_hist.rename(columns={'date': 'date'}, inplace=True)

        # 3. 시가총액 추정: 최신 시가총액 기반 비례계산
        latest_market_cap = vti.info['marketCap']
        latest_price = vti.info['previousClose']
        shares_outstanding = latest_market_cap / latest_price

        # 시가총액 추정
        vti_hist['vti_market_cap'] = vti_hist['vti_price'] * shares_outstanding

        # 4. 지수 계산
        merged = pd.merge(vti_hist, m2, on='date', how='left')
        merged['m2_per_marketcap'] = merged['m2'] / merged['vti_market_cap']
        merged.dropna(inplace=True)

        # Dataset 반환
        datasets = [{
            "data": merged[data_column].tolist(),
            "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(merged["date"]).tolist()],
            "legend_label": legend_label
        }]
        return datasets


class FredIndex:
    def __init__(self, ticker, diff_year):
        self.ticker = ticker
        self.end_date = datetime.datetime.today()
        self.start_date = self.end_date - datetime.timedelta(days=365 * diff_year)

    def get_data(self, data_column, legend_label):
        cpi = web.DataReader(self.ticker, 'fred', self.start_date, self.end_date)
        cpi = cpi.reset_index()
        cpi.rename(columns={'DATE': 'date'}, inplace=True)

        # 정규화 (처음 값을 100으로)
        cpi_base = cpi[self.ticker].iloc[0]
        cpi['Normed'] = cpi[self.ticker] / cpi_base * 100

        # Dataset 반환
        datasets = [{
            "data": cpi[data_column].tolist(),
            "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(cpi["date"]).tolist()],
            "legend_label": legend_label
        }]
        return datasets
