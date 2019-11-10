import pandas as pd

class Reports():
	def __init__(self, db):
		self.db = db

	def create_report(self, func):
		function = getattr(self, func)
		function()

	def order_fulfilment_duration_report(self):
		result = self.db["events"].find({
				"order_fulfilment": 1
			})
		df = pd.DataFrame(list(result))
		del df["_id"]
		df['duration'] = pd.to_datetime(df['order_last_time']) - pd.to_datetime(df['order_start_time'])
		df['duration'] = df['duration'].astype('timedelta64[m]')

		new_list = []
		new_list.append({'duration':'duration < 5 mins', 'count':len(df[df['duration'] < 5])})
		new_list.append({'duration':'5 >= duration < 10', 'count':len(df[(df['duration'] >= 5) & (df['duration'] < 10)])})
		new_list.append({'duration':'10 >= duration < 20', 'count':len(df[(df['duration'] >= 10) & (df['duration'] < 20)])})
		new_list.append({'duration':'20 >= duration < 30', 'count':len(df[(df['duration'] >= 20) & (df['duration'] < 30)])})
		new_list.append({'duration':'30 >= duration < 40', 'count':len(df[(df['duration'] >= 30) & (df['duration'] < 40)])})
		new_list.append({'duration':'40 >= duration < 50', 'count':len(df[(df['duration'] >= 40) & (df['duration'] < 50)])})
		new_list.append({'duration':'50 >= duration < 60', 'count':len(df[(df['duration'] >= 50) & (df['duration'] < 60)])})
		new_list.append({'duration':'duration >= 60 mins', 'count':len(df[df['duration'] >= 60])})
		
		self.db["order_fulfilment_duration_collection"].remove({})
		self.db["order_fulfilment_duration_collection"].insert(new_list)

	def open_orders_report(self):
		result = self.db["events"].find({
				"$or":[ {"order_status":2}, {"order_fulfilment":2}]
			})
		count = self.db["events"].find().count()

		self.db["open_orders_collection"].remove({})
		self.db["open_orders_collection"].insert({"open_orders": len(list(result)), "closed_orders": count-len(list(result))})

	def cancelled_orders_over_age_report(self):
		result = self.db["events"].find({
				"order_fulfilment": 0
			},{"customer_age": 1, "_id": 0})
		
		df = pd.DataFrame(list(result))

		new_list = []
		new_list.append({'customer_age':'age < 18', 'canelled_orders':len(df[df['customer_age'] < 18]), 'cancelled_orders_probability':(len(df[df['customer_age'] < 18])/float(len(df)))*100})
		new_list.append({'customer_age':'18 >= customer_age < 30', 'canelled_orders':len(df[(df['customer_age'] >= 18) & (df['customer_age'] < 30)]), 'cancelled_orders_probability':(len(df[(df['customer_age'] >= 18) & (df['customer_age'] < 30)])/float(len(df)))*100})
		new_list.append({'customer_age':'30 >= customer_age < 40', 'canelled_orders':len(df[(df['customer_age'] >= 30) & (df['customer_age'] < 40)]), 'cancelled_orders_probability':(len(df[(df['customer_age'] >= 30) & (df['customer_age'] < 40)])/float(len(df)))*100})
		new_list.append({'customer_age':'40 >= customer_age < 50', 'canelled_orders':len(df[(df['customer_age'] >= 40) & (df['customer_age'] < 50)]), 'cancelled_orders_probability':(len(df[(df['customer_age'] >= 40) & (df['customer_age'] < 50)])/float(len(df)))*100})
		new_list.append({'customer_age':'50 >= customer_age < 60', 'canelled_orders':len(df[(df['customer_age'] >= 50) & (df['customer_age'] < 60)]), 'cancelled_orders_probability':(len(df[(df['customer_age'] >= 50) & (df['customer_age'] < 60)])/float(len(df)))*100})
		new_list.append({'customer_age':'customer_age >= 60', 'canelled_orders':len(df[df['customer_age'] >= 60]), 'cancelled_orders_probability':(len(df[df['customer_age'] >= 60])/float(len(df)))*100})

		self.db["cancelled_orders_over_age_collection"].remove({})
		self.db["cancelled_orders_over_age_collection"].insert(new_list)


