import time
from mongodb import MongoDB
from processfile import ProcessFile
from watchdog.observers import Observer

if __name__ == "__main__":
	#Connection with MongoDB
	mongo_instance = MongoDB("mongodb://127.0.0.1/", 27017)
	mongo_client = mongo_instance.connect()
	db = mongo_instance.get_db(mongo_client, "mydb")
	collection = mongo_instance.get_collection(db, "events")

	observer = Observer()
	event_handler = ProcessFile(db) # create event handler
	observer.schedule(event_handler, path='./SOURCE_FILES')
	observer.start()

	print("Waiting for File.")
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
		observer.join()

