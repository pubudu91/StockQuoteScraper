import scrapy

class StockQuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://www.nasdaq.com/symbol/goog/real-time',
            'http://www.nasdaq.com/symbol/ibm/real-time',
            'http://www.nasdaq.com/symbol/twtr/real-time'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        stock_quote = response.css('#qwidget-quote-wrap')

        yield {
            'timestamp' : stock_quote.css('#qwidget_markettime::text').extract_first().strip(),
            'symbol' : stock_quote.css('div.qwidget-symbol::text').extract_first().strip(),
            'price' : stock_quote.css('#qwidget_lastsale::text').re_first(r'\d+\.?\d*'),
            'high' : response.css('#quotes_content_left__TodaysHigh::text').re_first(r'\d+\.?\d*'),
            'low' : response.css('#quotes_content_left__TodaysLow::text').re_first(r'\d+\.?\d*')
        }
