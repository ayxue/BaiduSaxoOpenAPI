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

    def Balance(self):
        client = self.GetHttpClient()
        ret = client.get('/port/v1/balances/me')
        return Utils.DicToObj("Balance", json.loads(ret))

    def Charts(self, uic, assetType, horizon, fromTime):
        client = self.GetHttpClient()
        url = '/chart/v1/charts/?AssetType={0}&Horizon={1}&Mode=From&Time={2}&Uic={3}'.format(assetType, horizon, fromTime, uic)
        ret = client.get(url)
        retObj = json.loads(ret)
        return Utils.DicToObjList("ChartData", retObj["Data"])



