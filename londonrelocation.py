from re import split
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        # Write your code here and remove `pass` in the following line
        pages = response.xpath('.//div[contains(@class,"pagination")]//a/@href').extract()

        '''print('\n'*5)
        print(pages)
        print('\n'*5)'''

        for i in range(0,2):
            if i<len(pages)-1:
                yield Request(url=pages[i],
                          callback=self.parse_properties_pages)

        
    def parse_properties_pages(self,response):
        titles = response.xpath('.//div[contains(@class,"test-inline")]//h4/a//text()').extract()
        prices = response.xpath('.//div[contains(@class,"test-inline")]//h5//text()').extract()
        urls = response.xpath('.//div[contains(@class,"test-inline")]//h4/a/@href').extract()
        
        for (title,price,url) in zip(titles,prices,urls):
            property = ItemLoader(item=Property())
            property.add_value('title', title.strip())
            splitPrice = price.strip().split()
            price_To_be_saved = int(splitPrice[1])
            if splitPrice[2]=='pw':
                price_To_be_saved *= 4

            property.add_value('price', str(price_To_be_saved)) #all per month
            property.add_value('url', 'https://londonrelocation.com'+url.strip())
            
        return property.load_item()

    
