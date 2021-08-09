import pymongo


class MongoPipeline(object):
    collection_name = 'wikipedia'  # collection name of database

    def __init__(self, mongo_uri, mongo_db):  # constructor function
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    # Function to retrieve the information specified in settings.py
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    # initializes the spider and makes connection with MongoDB
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # Closes spider
    def close_spider(self, spider):
        self.client.close()

    # insert the item to the database
    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item