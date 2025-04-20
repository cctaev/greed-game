import requests

BASE_URL = "https://yunhq.sse.com.cn:32042/v1/sh1/line/{}"


resp = requests.get(
    url=BASE_URL.format(600006),
    params={
        "callback": "jQuery371020392959715575865_1745069760720",
        "select": "time,price,volume,avg_price,amount,highest,lowest",
        "_": 1745069760721
    }
)

print(resp.text)