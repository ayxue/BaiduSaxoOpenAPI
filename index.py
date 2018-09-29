# -*- encoding=utf-8 -*-
import sys
from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from saxo.OpenApi import OpenApi
from datetime import datetime
from datetime import timedelta

reload(sys)
sys.setdefaultencoding('utf8')

class SaxoBot(Bot):

    def __init__(self, request_data):
        super(SaxoBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('InfoPrice', self.getInfoPrice)
        self.add_intent_handler('Greeting', self.Greeting)
        self.add_intent_handler('Balance', self.Balance)
        self.token = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IkQ2QzA2MDAwMDcxNENDQTI5QkYxQTUyMzhDRUY1NkNENjRBMzExMTcifQ.eyJvYWEiOiI3Nzc3NyIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiY2lkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiNGNhMWQ4ZmY5ZTFiNDI2NGE5MTU0OGVhOGI2ZmJmMDIiLCJkZ2kiOiI4NCIsImV4cCI6IjE1MzgyNzM1ODMifQ.GWmH2jxgUQ5kI-3R0iW3xC_6BovICTVvDXMJpgA6J_SvY9zRVGBVyuXb4A4Zn1aLUm2NbNeGcuRaMTfXGwbgSw'

    def launch_request(self):
        """
        打开调用名
        """

        self.wait_answer()
        myName = OpenApi(self.token).Client().Name
        renderTemplate = self.getTemplate("SAXO", "欢迎使用盛宝平台")
        return {
            'directives': [renderTemplate],
            'outputSpeech': '大家好，我是盛宝。{0}, 你好.'.format(myName)
        }
    
    def Greeting(self):
        myName = OpenApi(self.token).Client().Name
        renderTemplate = self.getTemplate( "你好, {0}, 我是盛宝".format(myName), "打招呼")
        return {
                'directives': [renderTemplate],
                'outputSpeech': '你好, {0}, 盛宝在这里'.format(myName)
            }

    def Balance(self):
        balance = OpenApi(self.token).Balance()
        cashAvailable = balance.CashBalance - balance.TransactionsNotBooked
        accountValue = balance.TotalValue
        unit = "美元"
        if balance.Currency == "EUR":
            unit = "欧元"
        
        content = "账户总值: {0}{1}, 可用现金：{2}{1}".format(accountValue, unit, cashAvailable)
        renderTemplate = self.getTemplate( content, "查余额")
        return {
                'directives': [renderTemplate],
                'outputSpeech': content
            }

    # 询价
    def getInfoPrice(self):
        uic = self.get_slots('Instrument')
        if not uic:
            self.nlu.ask('Instrument')
            renderTemplate = self.getTemplate(r'需要查哪个产品', '')

            return {
                'directives': [renderTemplate],
                'reprompt': r'需要查哪个产品',
                'outputSpeech': r'需要查哪个产品'
            }

        result = self.QueryInfoPrice(uic)
        title = '{0} - {1}\n'.format( result['time'], result['name'])
        content = title
        for prop in result['props']:
            content = content + '{0} {1}\n'.format(prop['name'], prop['value'])
        renderTemplate = self.getTemplate(content, title)
        return {
            'directives': [renderTemplate],
            'outputSpeech': content
        }

    def getTemplate(self, content, title = ""):
        template = BodyTemplate1()
        template.set_title(title)
        template.set_plain_text_content(content)
        template.set_background_image('https://gss0.bdstatic.com/-4o3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268/sign=644d464dab18972ba33a07ccdecc7b9d/cefc1e178a82b901fecbb96a738da9773912ef01.jpg')
        template.set_token('e9f72c66-78da-3236-5222-d460e5de2509')
        renderTemplate = RenderTemplate(template)
        return renderTemplate

    def QueryInfoPrice(self, uic):
        openApi = OpenApi(self.token)
        fromTime = datetime.strftime(datetime.utcnow() - timedelta(days = 1), "%Y-%m-%dT00:00:00Z")
        prices = openApi.Charts(uic, 'FxSpot', '1440', fromTime)
        price = prices[len(prices) - 1]
        date = datetime.strptime(price.Time, '%Y-%m-%dT%H:%M:%S.%fZ')

        name = '美元兑人民币'
        if uic == '52830':
            name = '欧元兑人民币'

        return {
            'name': name,
            'props':[
                {
                    'name':'中间价',
                    'value': (price.CloseAsk + price.CloseBid) / 2
                }
             ],
            'time':'{0}月{1}日'.format(date.month, date.day)
        }


def handler(event, context):
    bot = SaxoBot(event)
    result = bot.run()
    return result

