import scrapy
from scrapy import Selector
from scrapy_splash import SplashRequest
from ..items import MedicalkgItem


class BaikemedicalSpider(scrapy.Spider):
    name = 'BaikeMedical'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/wikitag/taglist?tagId=75956']
                  # 'https://baike.baidu.com/wikitag/taglist?tagId=75954',
                  # 'https://baike.baidu.com/wikitag/taglist?tagId=75955',
                  # 'https://baike.baidu.com/wikitag/taglist?tagId=75956']
    triple_cnt = 0

    def start_requests(self):
        scripts = """
            function main(splash, args)
                splash:go(args.url)
                splash:wait(0.3)
                local cur_height = splash:evaljs("document.body.scrollTop")
                local scrollHeight = splash:evaljs("document.body.scrollHeight")
                local prev_height = 0
                local torrent = 10
                local lag_cnt = 0
                while(cur_height < scrollHeight)
                do
                    splash:evaljs("window.scrollTo(0, document.body.scrollHeight)")
                    splash:wait(0.2)
                    prev_height = cur_height
                    cur_height = splash:evaljs("document.body.scrollTop")
                    splash:wait(0.1)
                    scrollHeight = splash:evaljs("document.body.scrollHeight")
                    splash:wait(0.1)
                    print(cur_height, scrollHeight)
                    if prev_height == cur_height then
                        lag_cnt = lag_cnt + 1
                        if lag_cnt == torrent then
                            break
                        end
                    end
                end
                return {
                    html = splash:html()
                }
            end
        """
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                endpoint='execute',
                                args={
                                    'lua_source': scripts,
                                    'timeout': 90
                                })

    def parse_second_page(self, response):
        page_target = response.xpath('//dl[@class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"]/dd/h1/text()').extract_first()
        blocks = response.xpath('//div[@class="basic-info J-basic-info cmn-clearfix"]/dl')
        for block in blocks:
            names = block.xpath('./dt/text()').extract()
            values = block.xpath('./dd/text()').extract()
            for name, value in zip(names, values):
                name = name.strip('\n').replace('\xa0', '').replace(' ', '')
                value = value.strip('\n').replace('\xa0', '').replace(' ', '')
                if len(value) == 0:
                    continue
                new_item = MedicalkgItem()
                new_item['head'] = page_target
                new_item['relation'] = name
                new_item['tail'] = value
                self.triple_cnt += 1
                if self.triple_cnt % 1000 == 0:
                    print(self.triple_cnt)
                yield new_item

    def parse(self, response):
        urls = response.xpath('//div[@class="waterFall_item "]/a/@href').extract()
        print(len(urls))
        for url in urls:
            yield SplashRequest(url=url,
                                callback=self.parse_second_page,
                                )
