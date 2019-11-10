import json
import os
from watchdog.events import FileSystemEventHandler
from fileactions import FileActions
from reports import Reports

class ProcessFile(FileSystemEventHandler):
	def __init__(self, db):
		self.db = db

	def on_created(self, event):
		print "Recieved File %s" % event.src_path
		filename = event.src_path
		orders_action = {
			"customer_registered":"customer_registered",
			"product_ordered":"product_ordered",
			"order_declined":"order_declined",
			"order_accepted":"order_accepted",
			"order_cancelled":"order_cancelled",
			"order_fulfilled":"order_fulfilled"
		}
		reports_list = [
			"order_fulfilment_duration_report",
			"open_orders_report",
			"cancelled_orders_over_age_report"
		]
		file_actions = FileActions(self.db)
		reports = Reports(self.db)

		with open(filename) as json_file:
			data = json.load(json_file)

			for d in data:
				file_actions.action(orders_action[d["type"]], d)
			#list_values = [ v for v in row.values() ]
			#self.db["events"].insert(list_values)
			os.remove(filename)
		
		for rl in reports_list:
			reports.create_report(rl)

		print("Waiting for File.")	


