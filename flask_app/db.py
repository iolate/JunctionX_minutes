__all__ = ['get_db']

from flask import current_app, g

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		import sqlite3
		db = g._database = sqlite3.connect(current_app.config.get('DATABASE', 'database.db'))
		db.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
		
		init_db(db)
		
	return db

def init_db(db=None):
	with current_app.app_context():
		if db is None: db = get_db()
		with current_app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
