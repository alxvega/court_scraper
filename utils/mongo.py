import logging
from pymongo import MongoClient

logger = logging.basicConfig(filename='test.log', level=logging.INFO)


username = password = 'admin'
def insert_bulk(documents, collection):
    with MongoClient('0.0.0.0:27017', 27017,username=username,password=password) as cliente:
        db = cliente.delaware_court

        result = db[collection].bulk_write(documents)
        bulk_api_result = result.bulk_api_result
        logging.info(f''
              f'Insert: {bulk_api_result["nUpserted"]} - '
              f'Matched:  {bulk_api_result["nMatched"]} - '
              f'Modified: {bulk_api_result["nModified"]}'
              )
