import scrapy

class KiasuSpider(scrapy.Spider):
    name = 'hwzscrape'

    start_urls = [
        'https://forums.hardwarezone.com.sg/forums/pc-gaming.382/',
    ]

    def parse(self, response):
        for thread in response.xpath('//div[@class="structItem-title"]'):
            yield response.follow(thread.xpath('a/@href').get(), self.parse_post)

        next_page = response.xpath('//a[@class="pageNav-jump pageNav-jump--next"][1]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        username = response.xpath('//h4[@class="message-name"]/a/text()').extract_first()
        if username == None:
            username = response.xpath('//h4[@class="message-name"]/a/span/text()').extract_first()

        yield {
            'post_topic': response.xpath('//h1[@class="p-title-value"]/text()').get(),
            'user' : username,
            "contents": response.xpath('string(//div[@class="bbWrapper"])').get()
        }