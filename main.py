from saxo.OpenApi import OpenApi
import json
from collections import namedtuple
from datetime import datetime
from datetime import timedelta
from saxo.Chatbot import Chatbot


#print(datetime.utcnow().month)
#token = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IkQ2QzA2MDAwMDcxNENDQTI5QkYxQTUyMzhDRUY1NkNENjRBMzExMTcifQ.eyJvYWEiOiI3Nzc3NyIsImlzcyI6Im9hIiwiYWlkIjoiMTEwIiwidWlkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiY2lkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiaXNhIjoiVHJ1ZSIsInRpZCI6IjIwMDIiLCJzaWQiOiI2NTYwNTk4MTE5OGY0NDc4OTBjZjVjY2Y4ZmM1NmY5YiIsImRnaSI6IjgyIiwiZXhwIjoiMTU2MzUyMTU5NyJ9.ThYE2HaYVylTNJ003Jt5ft5IaPWpbctqqXH6A0l4XoFOdcJfOPtdE1wuTx-taHYgGTDcSu-W1f8QoTWAtW_nYg'
#openApi = OpenApi(token)
#apps = openApi.GetApps()
#print(apps.__len__)
#print(apps[apps.__len__() - 1].Name)

#openApi.CreateApp('Test App1')
#apps = openApi.GetApps()
#print(apps.__len__)

chatbot = Chatbot()
me = chatbot.Client()
actionList = chatbot.Chat("盛宝银行在哪里")
action = actionList[0].say


#client = openApi.Client()
#balance = openApi.Balance()
#strClient = json.dumps(client)
#fromTime = datetime.strftime(datetime.utcnow() - timedelta(days = 1), "%Y-%m-%dT00:00:00Z")
#prices = openApi.InfoPrice(52870, 'FxSpot')

#accountKey = openApi.Accounts()[0].AccountKey
#ret = openApi.TradeAsMarket( 52870, 1000, "FxSpot", accountKey, "Buy")
#orderId = ret.OrderId


#netPosition = openApi.NetPositions()
#instrumentCount = netPosition.InstrumentCount
#pnl = netPosition.PnL
#cost = netPosition.Cost

