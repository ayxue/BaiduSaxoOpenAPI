from saxo.OpenApiHttpClient import OpenApiHttpClient
from saxo.Utils import Utils
import json

class OpenApi:
    def __init__(self, token):
        self.token = token
        self.host = 'gateway.saxobank.com'
        self.protocol = 'https'
        self.baseUrl = '{0}://{1}{2}'.format(self.protocol, self.host, '/sim/openapi')

    def GetHttpClient(self):
        return OpenApiHttpClient(self.host, self.protocol, self.baseUrl, self.token)

    def Client(self):
        client = self.GetHttpClient()
        ret = client.get('/port/v1/users/me')
        return Utils.DicToObj("Client", json.loads(ret))
    
    def TradeAsMarket(self, uic, amount, assetType, accountKey, action): 
        client = self.GetHttpClient()
        param = { 
            "Uic": uic,
            "BuySell": action,
            "AssetType": assetType,
            "Amount": amount,
            "OrderType": "Market",
            "OrderRelation": "StandAlone",
            "OrderDuration": {
                "DurationType": "DayOrder"
            },
            "AccountKey": accountKey
        }
        body = json.dumps(param)
        ret = client.post('/trade/v2/orders', body)
        return Utils.DicToObj("OrderId", json.loads(ret))

    def NetPositions(self): 
        client = self.GetHttpClient()
        ret = client.get('/port/v1/netpositions/me/')
        retObj = json.loads(ret)
        ret = {
            'Currency': 'Euro',
            'PnL': 0.00,
            'Cost': 0.00,
            'InstrumentCount': 0
        }

        for position in retObj["Data"]:
            ret["InstrumentCount"] = ret["InstrumentCount"] + 1
            #ret["PnL"] = ret["PnL"] + position["NetPositionView"]["ProfitLossOnTradeInBaseCurrency"]
            #ret["Cost"] = ret["Cost"] + position["NetPositionView"]["TradeCostsTotalInBaseCurrency"]

        return Utils.DicToObj("NetPositions", ret)


    def Balance(self):
        client = self.GetHttpClient()
        ret = client.get('/port/v1/balances/me')
        return Utils.DicToObj("Balance", json.loads(ret))

    def Accounts(self):
        client = self.GetHttpClient()
        ret = client.get('/port/v1/accounts/me/')
        retObj = json.loads(ret)
        return Utils.DicToObjList("Accounts", retObj["Data"])

    def InfoPrice(self, uic, assetType):
        client = self.GetHttpClient()
        url = '/trade/v1/infoprices/?AssetType={0}&Uic={1}'.format(assetType, uic)
        ret = json.loads(client.get(url))
        shell = Utils.DicToObj("InfoPrice", ret)
        return shell

    def Charts(self, uic, assetType, horizon, fromTime):
        client = self.GetHttpClient()
        url = '/chart/v1/charts/?AssetType={0}&Horizon={1}&Mode=From&Time={2}&Uic={3}'.format(assetType, horizon, fromTime, uic)
        ret = client.get(url)
        retObj = json.loads(ret)
        return Utils.DicToObjList("ChartData", retObj["Data"])

    def GetApps(self):
        client = self.GetHttpClient()
        url = '/developer/apps'
        ret = client.get(url)
        retObj = json.loads(ret)
        return Utils.DicToObjList("AppData", retObj["Data"])


    def CreateApp(self, name):
        client = self.GetHttpClient()
        param = { 
            "Description": name,
            "Flow": "Code",
            "Name": name
        }
        body = json.dumps(param)
        client.post('/developer/apps', body)
        return


