from saxo.OpenApi import OpenApi
import json
from collections import namedtuple
from datetime import datetime
from datetime import timedelta

print(datetime.utcnow().month)
token = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IkQ2QzA2MDAwMDcxNENDQTI5QkYxQTUyMzhDRUY1NkNENjRBMzExMTcifQ.eyJvYWEiOiI3Nzc3NyIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiY2lkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiNGNhMWQ4ZmY5ZTFiNDI2NGE5MTU0OGVhOGI2ZmJmMDIiLCJkZ2kiOiI4NCIsImV4cCI6IjE1MzgyNzM1ODMifQ.GWmH2jxgUQ5kI-3R0iW3xC_6BovICTVvDXMJpgA6J_SvY9zRVGBVyuXb4A4Zn1aLUm2NbNeGcuRaMTfXGwbgSw'
openApi = OpenApi(token)
client = openApi.Client()
balance = openApi.Balance()
#strClient = json.dumps(client)
fromTime = datetime.strftime(datetime.utcnow() - timedelta(days = 1), "%Y-%m-%dT00:00:00Z")
prices = openApi.Charts(52870, 'FxSpot', '1440', fromTime)
price2 = prices[len(prices) - 1]
for price in prices:
    #keys = list(price.keys())
    #vals = list(price.values())
    #Data = namedtuple('data', keys)
    #obj = Data._make(vals)
    #dic = obj._asdict()
    print(price)
    #obj = {}
    #obj.__dict__.update(dict)
    #print(obj)
#strClient = json.dumps(chart)
#print(strClient)