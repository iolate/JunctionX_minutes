import sqlite3
import Speech2Text
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

def get_pending_one(db):
	cursor = db.cursor()
	cursor.execute('''SELECT
			`idx`, `name`, `status`, `filename`, `filesize`, `created_at`, `is_private`
		FROM `minutes` WHERE `status` = ?;''', ('pending',))
	return cursor.fetchone()

def set_status(db, idx, status):
	db.cursor().execute('UPDATE `minutes` SET `status` = ? WHERE `idx` = ?;', (status, idx))
	db.commit()

def cronjob(config):
	db = sqlite3.connect(config.get('DATABASE', 'database.db'))
	db.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
	
	row = get_pending_one(db)
	if row is None:
		db.close()
		return False
	
	try:
		set_status(db, row['idx'], 'processing')
		
		fp = os.path.join(config.get('UPLOAD_DIR', 'upload'), row['filename'])
		result = Speech2Text.Speech2Text(fp, config)
		print('{}/{} done.'.format(row['idx'], row['name']))
		
		db.cursor().execute('UPDATE `minutes` SET `status` = ?, `scripts` = ? WHERE `idx` = ?;', ('processing', json.dumps(result), row['idx']))
		db.commit()
	except:
		print('{}/{} error')
		raise
		
		set_status(db, row['idx'], 'error')
		db.close()
		return False
	
	db.close()
	return True

if __name__ == '__main__':
	import time
	config = load_config('flask_app/settings.cfg')
	
	'''while True:
		if cronjob(config):
			pass
		else:
			time.sleep(3)'''

# ----------

def remove(db, idx, config):
	import os
	
	cursor = db.cursor()
	cursor.execute('''SELECT
			`idx`, `name`, `status`, `filename`, `filesize`, `created_at`, `is_private`
		FROM `minutes` WHERE `idx` = ?;''', (idx,))
	row = cursor.fetchone()
	
	fp = os.path.join(config.get('UPLOAD_DIR', 'upload'), row['filename'])
	if os.path.exists(fp):
		os.remove(fp)
	
	cursor.execute('DELETE FROM `minutes` WHERE `idx` = ?;', (idx,))
	db.commit()