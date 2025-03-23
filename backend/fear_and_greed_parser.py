from datetime import datetime

import requests
import pandas as pd


class FearAndGreed:
    def __init__(self, diff_year):
        self.diff_year = diff_year  # 3년이 안정적
        self.data_columns = ['fear_and_greed_historical',
                             'market_momentum_sp500',
                             'market_momentum_sp125',
                             'put_call_options',
                             'market_volatility_vix',
                             'safe_haven_demand']
        self.data = self._get_period_data()
        self.df = self._fear_and_greed_preprocess()

    def _get_period_data(self):
        today = datetime.today()

        # N년 전 날짜 계산
        three_years_ago = today.replace(year=today.year - self.diff_year)

        # "YYYY-MM-DD" 형식으로 변환
        formatted_date = three_years_ago.strftime("%Y-%m-%d")

        # URL & header 지정
        base_url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        start_date = formatted_date
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        # get response
        response = requests.get("{}/{}".format(base_url, start_date), headers=headers)
        data = response.json()
        return data

    def _fear_and_greed_preprocess(self):
        # 데이터 정리
        parsed_data = {
            col: {
                datetime.utcfromtimestamp(entry["x"] / 1000).strftime("%Y-%m-%d"): entry["y"]
                for entry in self.data[col]["data"]
            }
            for col in self.data_columns
        }

        # 날짜 리스트 추출 (모든 컬럼의 날짜를 포함)
        all_dates = sorted(set(date for col in parsed_data.values() for date in col.keys()))

        # 데이터프레임 생성
        df = pd.DataFrame({"date": all_dates})

        # 컬럼별 데이터 매핑
        for col in self.data_columns:
            df[col] = df["date"].map(parsed_data[col])

        # 날짜 정렬
        df = df.sort_values(by="date")

        # NaN이 있는 행(row) 전체 삭제
        df_cleaned = df.dropna()

        # date type
        df_cleaned.loc[:, "date"] = pd.to_datetime(df_cleaned["date"])
        return df_cleaned

    def get_current_status(self):
        # 이모티콘 표현 로직
        def get_fear_and_greed_info(str_score, rating):
            score = float(str_score)
            if score >= 76:
                emoji = "🚀"
            elif score >= 56:
                emoji = "🤑"
            elif score >= 46:
                emoji = "😐"
            elif score >= 26:
                emoji = "😭"
            else:
                emoji = "🤬"
            return f"{emoji} {rating} ( 📉 {score:.2f} )"

        sub_title = get_fear_and_greed_info(self.data['fear_and_greed']['score'], self.data['fear_and_greed']['rating'])
        return sub_title

    def get_data(self, data_column, legend_label):
        datasets = [{
            "data": self.df[data_column].tolist(),
            "labels": [dt.strftime('%Y-%m-%d') for dt in pd.to_datetime(self.df["date"]).tolist()],
            "legend_label": legend_label
        }]
        return datasets
