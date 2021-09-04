# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicalkgItem(scrapy.Item):
    # define the fields for your item here like:
    head = scrapy.Field()
    relation = scrapy.Field()
    tail = scrapy.Field()
    pass
