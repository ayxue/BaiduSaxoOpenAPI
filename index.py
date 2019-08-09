# -*- encoding=utf-8 -*-
import sys
from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from saxo.OpenApi import OpenApi
from datetime import datetime
from datetime import timedelta
from dueros.card.TextCard import TextCard
from saxo.Chatbot import Chatbot

reload(sys)
sys.setdefaultencoding('utf8')

class SaxoBot(Bot):

    def __init__(self, request_data):
        super(SaxoBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('InfoPrice', self.getInfoPrice)
        self.add_intent_handler('Greeting', self.Greeting)
        self.add_intent_handler('Balance', self.Balance)
        self.add_intent_handler('Trade', self.Trade)
        self.add_intent_handler('NetPositions', self.NetPositions)
        self.add_intent_handler('Bye', self.Bye)
        self.add_intent_handler('GetApps', self.GetApps)
        self.add_intent_handler('CreateApp', self.CreateApp)
        self.add_intent_handler('ai.dueros.common.default_intent',self.Chat)
        self.reprompt ='需要我做什么'
        self.token = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IkQ2QzA2MDAwMDcxNENDQTI5QkYxQTUyMzhDRUY1NkNENjRBMzExMTcifQ.eyJvYWEiOiI3Nzc3NyIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiY2lkIjoiZFg4NzBzYTJkaXVVMWRjSTVlfGtjQT09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiMGVlOWJlNTY4NjEzNGMxOGEzNGY0OGM0MTc3ZjhhNjIiLCJkZ2kiOiI4NCIsImV4cCI6IjE1NjQ4MDUzMTMifQ.FY_WEMo7Jv5Z5yEf-sQMxVQwFYbphRLQC8GXWdQKhL8cqgv4E8aIkd7vNxPgQAp9cGXSeGfQdzBGcZmKNyNikQ'

    def launch_request(self):
        """
        打开调用名
        """

        self.wait_answer()
        myName = OpenApi(self.token).Client().Name
        renderTemplate = self.getTemplate("SAXO", "欢迎使用盛宝开放银行")
        return {
            'directives': [renderTemplate],
            'outputSpeech': '大家好，我是盛小宝。{0}, 欢迎使用开放银行平台.'.format(myName)
        }
    
    def Greeting(self):
        self.wait_answer()
        myName = OpenApi(self.token).Client().Name
        renderTemplate = self.getTemplate( "你好, {0}, 我是盛小宝".format(myName), "打招呼")
        return {
                'directives': [renderTemplate],
                'outputSpeech': '你好, {0}, 欢迎使用盛小宝开放银行平台'.format(myName)

            }
    
    def Chat(self):
        text = self.request.get_query()
        content = Chatbot().Chat(text)
        renderTemplate = self.getTemplate( content, "盛小宝智能问答")
        return {
                'directives': [renderTemplate],
                'outputSpeech': content
        }
    
    def Bye(self):
        myName = OpenApi(self.token).Client().Name
        renderTemplate = self.getTemplate( "不客气，再见".format(myName), "再见")
        return {
                'directives': [renderTemplate],
                'outputSpeech': '不客气，再见'.format(myName)
            }

    def Balance(self):
        self.wait_answer()
        balance = OpenApi(self.token).Balance()
        cashAvailable = balance.CashBalance + balance.TransactionsNotBooked
        accountValue = balance.TotalValue
        unit = "美元"
        if balance.Currency == "EUR":
            unit = "欧元"
        
        content = "账户总值: {0}{1}, 可用现金：{2}{1}".format(accountValue, unit, cashAvailable)
        renderTemplate = self.getTemplate( content, "查余额")
        card = TextCard(content)
        return {
                'card' : card,
                'outputSpeech': content
            }

    def NetPositions(self):
        self.wait_answer()
        openApi = OpenApi(self.token)
        netPosition = openApi.NetPositions()
        instrumentCount = netPosition.InstrumentCount
        pnl = netPosition.PnL
        cost = netPosition.Cost

        balance = OpenApi(self.token).Balance()
        marginPnl = balance.UnrealizedMarginProfitLoss
        nonMarginVal = balance.NonMarginPositionsValue
        exposure = balance.MarginNetExposure
        coverage = balance.MarginExposureCoveragePct

        remark = '风险低'
        if coverage <= 100:
            remark = '覆盖率比较低'

        content = "你有{0}支产品的仓位，股票等非保证金产品市值{1}欧元, 保证金产品风险敞口{2}欧元".format(instrumentCount, nonMarginVal, exposure)
        if instrumentCount == 0:
            content = '目前没有持仓'
        elif exposure > 0:
            content = content + '，目前保证金比率为{0}%, {1}'.format(coverage, remark)
        
        renderTemplate = self.getTemplate( content, "查仓位")
        card = TextCard(content)
        return {
                'card': card,
                'outputSpeech': content
            }

    
    def Trade(self):
        self.wait_answer()
        uic = self.get_slots('Instrument')
        action = self.get_slots('Actions')
        if not uic:
            self.nlu.ask('Instrument')
            renderTemplate = self.getTemplate(r'需要买什么', '')

            return {
                'directives': [renderTemplate],
                'reprompt': r'需要买什么',
                'outputSpeech': r'需要买什么'
            }

        assetType = self.get_slots('AssetType')
        if not assetType:
            assetType = 'FxSpot';
        
        amount = self.get_slots('Amount')
        if not amount:
            amount = self.get_slots('Quantity')
            if not amount:
                amount = 1000;

        openApi = OpenApi(self.token)
        accountKey = openApi.Accounts()[0].AccountKey
        ret = openApi.TradeAsMarket( uic, amount, assetType, accountKey, action)
        orderId = ret.OrderId

        content = "小宝已下交易指令，指令编号：" + orderId
        renderTemplate = self.getTemplate( content, "下指令")
        card = TextCard(content)
        return {
                'card': card,
                'outputSpeech': content
            }

    # 询价
    def getInfoPrice(self):
        self.wait_answer()
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
        card = TextCard(content)
        return {
            'card': card,
            'outputSpeech': content
        }

    def getTemplate(self, content, title = ""):
        template = BodyTemplate1()
        template.set_title(title)
        template.set_plain_text_content(content)
        #template.set_background_image('https://gss0.bdstatic.com/-4o3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268/sign=644d464dab18972ba33a07ccdecc7b9d/cefc1e178a82b901fecbb96a738da9773912ef01.jpg')
        template.set_token('e9f72c66-78da-3236-5222-d460e5de2509')
        #renderTemplate = RenderTemplate(template)
        return template


    def QueryInfoPrice(self, uic):
        openApi = OpenApi(self.token)
        # fromTime = datetime.strftime(datetime.utcnow() - timedelta(days = 1), "%Y-%m-%dT00:00:00Z")
        # prices = openApi.Charts(uic, 'FxSpot', '1440', fromTime)
        # price = prices[len(prices) - 1]
        # date = datetime.strptime(price.Time, '%Y-%m-%dT%H:%M:%S.%fZ')
        price = openApi.InfoPrice(uic, 'FxSpot')
        date = datetime.strptime(price.LastUpdated, '%Y-%m-%dT%H:%M:%S.%fZ')

        name = '美元对人民币'
        if uic == '52830':
            name = '欧元对人民币'

        if uic == '52873':
            name = '人民币对日元'

        return {
            'name': name,
            'props':[
                {
                    'name':'中间价',
                    'value': price.Quote["Mid"]
                }
             ],
            'time':'{0}点{1}分{2}秒'.format(date.hour + 8, date.minute, date.second)
        }

    def GetApps(self):
        self.wait_answer()
        openApi = OpenApi(self.token)
        apps = openApi.GetApps()
        if apps.__len__() == 0:
            content = "目前你还没有App，可以创建一个"
        else:
            content = '现在你有{0}个App, 比如名字叫{1}的'.format( apps.__len__(), apps[0].Name)
        
        renderTemplate = self.getTemplate( content, "查App")
        card = TextCard(content)
        return {
            'card': card,
            'outputSpeech': content
        }

    def CreateApp(self):
        self.wait_answer()
        openApi = OpenApi(self.token)
        name = self.get_slots('name')
        if not name:
            self.ask('name')
            return {
                'outputSpeech': '请告诉我App的名称',
                'reprompt': '请告诉我App的名称'
            }

        openApi.CreateApp(name)
        ret = self.GetApps()
        
        content = '创建完成。' + ret['outputSpeech']
        renderTemplate = self.getTemplate( content, "创建App")
        card = TextCard(content)
        return {
            'card': card,
            'outputSpeech': content
        }


def handler(event, context):
    bot = SaxoBot(event)
    result = bot.run()
    return result

