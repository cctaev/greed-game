import csv
import json
import os.path
import time
from datetime import date

import requests

from spider.utils.sleep_util import sleeper

BASE_URL = "https://yunhq.sse.com.cn:32042/v1/sh1/line/{}"
MAX_RETRIES = 3  # 最大失败重试次数
RETRY_DELAY = 5  # 失败重试间隔时间（秒）

class SseStockLineSpider:
    def __init__(self, stock_codes):
        self._session = None
        self._stock_codes = stock_codes

    def execute(self):
        self._session = requests.Session()
        try:
            for stock_code in self._stock_codes:
                self._query_stock_line(stock_code)
                print(f"股票代码：{stock_code} 已完成")
                sleeper((10, 100), 'ms')
        finally:
            print(f"所有股票代码已完成")
            self._session.close()

    def _query_stock_line(self, stock_code):
        params = {
            "callback": "",
            "select": "time,price,volume,avg_price,amount,highest,lowest",
            "_": time.time()
        }
        resp = None
        for index in range(MAX_RETRIES):
            try:
                resp = self._session.get(BASE_URL.format(stock_code), params=params, timeout=10)
                if resp.status_code == 200:
                    break
            except Exception as e:
                print(f"请求失败，错误信息：{e}")
                if index < MAX_RETRIES - 1:
                    print(f"第 {index + 1} 次重试中...")
                    time.sleep(RETRY_DELAY)
        if resp or resp.status_code == 200:
            line_data = self._parse_jsonp_to_json(resp.text)
            self._write_json_to_file(line_data, f"{stock_code}.json")
        else:
            print(f"股票代码：{stock_code} 请求失败")

    @staticmethod
    def _parse_jsonp_to_json(jsonp_text) -> dict | list | None:
        if not jsonp_text or not jsonp_text.startswith("(") or not jsonp_text.endswith(")"):
            return None
        jsonp_text = jsonp_text[1:-1]
        return json.loads(jsonp_text)

    @staticmethod
    def _write_json_to_file(data, file_name):
        today = date.today().strftime("%Y%m%d")
        base_path = os.path.join(os.path.dirname(__file__), "data", today, file_name)
        os.makedirs(os.path.dirname(base_path), exist_ok=True)
        with open(base_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # 读取所有股票代码
    codes = []
    file_path = os.path.join(os.path.dirname(__file__), "GPLIST.csv")
    with open(file_path, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            codes.append(row[0])
    spider = SseStockLineSpider(codes)
    spider.execute()
