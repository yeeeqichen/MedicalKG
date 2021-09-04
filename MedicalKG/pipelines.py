# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


client = pymongo.MongoClient('localhost')
db = client.MedicalKG
collection = db.MedicalKG


class MedicalkgPipeline:
    def process_item(self, item, spider):
        document = {
            'head': item['head'],
            'relation': item['relation'],
            'tail': item['tail']
        }
        collection.update_one(document,
                              {
                                  '$setOnInsert': document,
                              },
                              upsert=True)
        return item
