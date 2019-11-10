from utils import get_age
from datetime import date

class FileActions():
	def __init__(self, db):
		self.age = 0
		self.db = db

	def action(self, func, d):
		function = getattr(self, func)
		function(d)

	def customer_registered(self, d):
		customer_birthdate = d["data"]["birthdate"]
		year = int(customer_birthdate[0:4])
		month = int(customer_birthdate[5:7])
		day = int(customer_birthdate[8:10])

		self.age = get_age(date(year, month, day))

	def product_ordered(self, d):
		check = self.db["events"].find_one({"aggregate_id":d["aggregate_id"]})
		if check:
			pass
		else:
			row2 = {}
			row2["aggregate_id"] = d["aggregate_id"]
			row2["product_name"] = d["data"]["name"]
			row2["customer_age"] = self.age
			row2["order_start_time"] = d["timestamp"]
			row2["order_last_time"] = d["timestamp"]
			row2["order_status"] = 2
			row2["order_fulfilment"] = 2
			self.db["events"].insert(row2)
			#row[d["aggregate_id"]] = row2

	def order_declined(self, d):
		row2 = self.db["events"].find_one({"aggregate_id":d["aggregate_id"]})
		row2["order_status"] = 0
		row2["order_fulfilment"] = 0
		row2["order_last_time"] = d["timestamp"]
		self.db["events"].update({"aggregate_id":row2["aggregate_id"]}, row2, True)

	def order_accepted(self, d):
		row2 = self.db["events"].find_one({"aggregate_id":d["aggregate_id"]})
		row2["order_status"] = 1
		row2["order_last_time"] = d["timestamp"]
		self.db["events"].update({"aggregate_id":row2["aggregate_id"]}, row2, True)

	def order_cancelled(self, d):
		row2 = self.db["events"].find_one({"aggregate_id":d["aggregate_id"]})
		row2["order_fulfilment"] = 0
		row2["order_last_time"] = d["timestamp"]
		self.db["events"].update({"aggregate_id":row2["aggregate_id"]}, row2, True)

	def order_fulfilled(self, d):
		row2 = self.db["events"].find_one({"aggregate_id":d["aggregate_id"]})
		row2["order_fulfilment"] = 1
		row2["order_last_time"] = d["timestamp"]
		self.db["events"].update({"aggregate_id":row2["aggregate_id"]}, row2, True)


