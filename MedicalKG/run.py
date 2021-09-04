"""todo:
    增加对数据库的支持，把爬取回来的数据入库(done)
    增加对爬取的数据的可视化
"""

from scrapy import cmdline

print(cmdline.execute('scrapy crawl BaikeMedical'.split()))