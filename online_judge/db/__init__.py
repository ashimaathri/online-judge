from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017
DBNAME = 'online_judge'

mongo_client = MongoClient(HOST, PORT)
db = mongo_client[DBNAME]
