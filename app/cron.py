import json
import os

def load_config(filename):
	# https://github.com/pallets/flask/blob/master/src/flask/config.py
	import types
	
	d = types.ModuleType("config")
	d.__file__ = filename
	
	with open(filename, mode="rb") as config_file:
		exec(compile(config_file.read(), filename, "exec"), d.__dict__)
	
	return {key: getattr(d, key) for key in dir(d) if key.isupper()}
config = load_config('flask_app/settings.cfg')

def get_db():
	import sqlite3
	db = sqlite3.connect(config.get('DATABASE', 'database.db'))
	db.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
	return db

def get_pending_one(db):
	cursor = db.cursor()
	cursor.execute('''SELECT
			`idx`, `name`, `status`, `filename`, `filesize`, `created_at`, `is_private`
		FROM `minutes` WHERE `status` = ?;''', ('pending',))
	return cursor.fetchone()

def set_status(db, idx, status):
	db.cursor().execute('UPDATE `minutes` SET `status` = ? WHERE `idx` = ?;', (status, idx))
	db.commit()

def cronjob():
	import Speech2Text
	
	db = get_db()
	
	row = get_pending_one(db)
	if row is None:
		db.close()
		return False
	
	print('{}/{} starting.'.format(row['idx'], row['name']))
	try:
		set_status(db, row['idx'], 'processing')
		
		fp = os.path.join(config.get('UPLOAD_DIR', 'upload'), row['filename'])
		result, duration = Speech2Text.Speech2Text(fp, config)
		
		duration = int(duration)
		db.cursor().execute('UPDATE `minutes` SET `status` = ?, `video_duration` = ?, `scripts` = ? WHERE `idx` = ?;', ('done', duration, json.dumps(result), row['idx']))
		db.commit()
		
		print('{}/{} done.'.format(row['idx'], row['name']))
	except:
		print('{}/{} error')
		raise
		
		set_status(db, row['idx'], 'error')
		db.close()
		return False
	
	db.close()
	return True

def loop():
	import time
	
	while True:
		if cronjob():
			pass
		else:
			time.sleep(3)

if __name__ == '__main__':
	pass
	#loop()
