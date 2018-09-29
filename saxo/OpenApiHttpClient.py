import httplib

class OpenApiHttpClient:
    
    def __init__(self, host, protocol, baseUrl, token):
        self.host = host
        self.token = token
        self.protocol = protocol
        self.baseUrl = baseUrl


    def getConnection(self):
        if self.protocol == "https":
            return httplib.HTTPSConnection(self.host)
        return httplib.HTTPSConnection(self.host)

    def get(self, serviceUrl):
        return self.request(serviceUrl, "GET")

    def post(self, serviceUrl, body):
        return self.request(serviceUrl, "POST", body)

    def request(self, serviceUrl, method, body = None):
        try:
            conn = self.getConnection()
            headers = {"AUTHORIZATION": "BEARER " + self.token}
            requestUrl = self.baseUrl + serviceUrl
            conn.request(method = 'GET', url = requestUrl, body = body, headers = headers)
            response = conn.getresponse()
            res = response.read()
            return res
        finally:
            conn.close


