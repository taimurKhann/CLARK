import pymongo as pm
from db import DB

class MongoDB(DB):
	
	def __init__(self, host, port):
		self.host = host
		self.port = port

	def connect(self):
		mongoClient = pm.MongoClient(host = self.host, port = self.port)
		return mongoClient

	def get_db(self, mongoClient, db):
		return mongoClient[db]

	def get_collection(self, db, collection):
		return db[collection]

	def get_order_fulfilment_records(self, db):
		duration = []
		order_counts = []
		text = []
		records = db["order_fulfilment_duration_collection"].find({})
		for item in list(records):
			duration.append(str(item['duration']))
			order_counts.append(item['count'])
			
		return duration, order_counts

	def get_open_orders_record(self, db):
		records = db["open_orders_collection"].find_one({})
		return (records["open_orders"], records["closed_orders"]), ("Open Orders", "Closed Orders")

	def get_cancelled_orders_by_age_report(self, db):
		customer_age = []
		cancellation_probability = []
		records = db["cancelled_orders_over_age_collection"].find({})
		for item in list(records):
			customer_age.append(str(item['customer_age']))
			cancellation_probability.append(item['cancelled_orders_probability'])
		
		return customer_age, cancellation_probability
