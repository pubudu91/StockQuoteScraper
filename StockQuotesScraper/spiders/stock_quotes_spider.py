import scrapy
import random

class StockQuotesSpider(scrapy.Spider):
    name = "quotes"

    # nasdaq100 = ['aal','aapl','adbe','adi','adp','adsk','akam','alxn','amat','amgn','amzn','atvi','avgo','bidu','biib','bmrn','ca','celg','cern','chkp','chtr','cmcsa','cost','csco','csx','ctas','ctrp','ctsh','ctxs','disca','disck','dish','dltr','ea','ebay','esrx','expe','fast','fb','fisv','fox','foxa','gild','goog','googl','has','holx','hsic','ilmn','incy','intc','intu','isrg','jd','khc','klac','lbtya','lbtyk','lila','lilak','lrcx','lvnta','mar','mat','mchp','mdlz','mnst','msft','mu','mxim','myl','nclh','nflx','ntes','nvda','nxpi','orly','payx','pcar','pcln','pypl','qcom','qvca','regn','rost','sbac','sbux','shpg','siri','stx','swks','symc','tmus','trip','tsco','tsla','txn','ulta','viab','vod','vrsk','vrtx','wba','wdc','xlnx','xray','yhoo']
    #
    # rndsample = [13, 28, 39, 3, 32, 36, 69, 70, 23, 106, 54, 5, 61, 12, 94, 38, 27, 80, 96, 105, 89, 103, 78, 82, 4, 62, 11, 67, 19, 7, 100, 42, 26, 53, 77, 9, 68, 79, 18, 30, 22, 81, 65, 102, 93, 55, 104, 90, 17, 10]

    symbols = ['bidu', 'ctxs', 'fisv', 'adi', 'dltr', 'expe', 'mxim', 'myl', 'csco', 'yhoo', 'khc', 'adsk', 'lvnta', 'avgo', 'tsco', 'fb', 'ctsh', 'pypl', 'txn', 'xray', 'stx', 'wdc', 'pcar', 'qvca', 'adp', 'mar', 'atvi', 'msft', 'chkp', 'alxn', 'vrsk', 'gild', 'ctrp', 'jd', 'payx', 'amgn', 'mu', 'pcln', 'cern', 'disck', 'cost', 'qcom', 'mdlz', 'wba', 'trip', 'klac', 'xlnx', 'swks', 'celg', 'amzn']

    def start_requests(self):
        # global symbols
        for symbol in self.symbols:
            yield scrapy.Request(url='http://www.nasdaq.com/symbol/' + symbol + '/real-time', callback=self.parse)

    def parse(self, response):
        stock_quote = response.css('#qwidget-quote-wrap')

        yield {
            'timestamp' : stock_quote.css('#qwidget_markettime::text').extract_first().strip(),
            'symbol' : str(response.request.url).split("/")[-2],
            'price' : stock_quote.css('#qwidget_lastsale::text').re_first(r'\d+\.?\d*'),
            'high' : response.css('#quotes_content_left__TodaysHigh::text').re_first(r'\d+\.?\d*'),
            'low' : response.css('#quotes_content_left__TodaysLow::text').re_first(r'\d+\.?\d*')
        }
