
from flask import *
from .db import *

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

'''
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)
'''

def api_returns(f):
	import json
	from functools import wraps
	@wraps(f)
	def decorated_function(*args, **kwargs):
		resp = make_response(json.dumps(f(*args, **kwargs)))
		resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
		resp.headers['Pragma'] = 'no-cache'
		
		return resp
	return decorated_function

##########################################################################################

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/test')
def test():
	flash('test')
	return redirect('/')

def make_row(row, cursor):
	try:
		scripts = json.loads(row['scripts'])
		for script in scripts:
			# escape
			text = script['text'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
		
			for kp in script['key_phrases']:
				text = text.replace(kp, '<b>{}</b>'.format(kp))
			script['html'] = text
		row['scripts'] = scripts
	except: pass
	
	from datetime import datetime
	row['created'] = datetime.fromtimestamp(row['created_at']).strftime('%Y-%m-%d')
	
	try:
		cursor.execute('SELECT `tag` FROM `minutes_tags` WHERE `minutes_idx` = ?', (row['idx'],))
		row['tags'] = [row['tag'] for row in cursor.fetchall()]
	except:
		row['tags'] = []
	

@app.route('/minutes/<int:idx>')
def minutes_view(idx):
	import json
	
	cursor = get_db().cursor()
	cursor.execute('SELECT * FROM `minutes` WHERE `idx` = ?;', (idx,))
	row = cursor.fetchone()
	if row is None: return abort(404)
	
	make_row(row, cursor)
	
	return render_template('view.html', row=row)

@app.route('/upload', methods=['GET'])
def upload():
	cursor = get_db().cursor()
	cursor.execute('SELECT `idx`, `name`, `status`, `filename`, `filesize`, `created_at`, `is_private` FROM `minutes`;')
	minutes = cursor.fetchall()
	
	return render_template('upload.html', minutes=minutes)

# ----------------------------------------

@app.route('/ajax/minutes/<int:idx>', methods=['POST'])
@api_returns
def ajax_minutes_update(idx):
	conn = get_db()
	cursor = conn.cursor()
	
	cursor.execute('SELECT filename FROM `minutes` WHERE `idx` = ?;', (idx,))
	row = cursor.fetchone()
	if row is None:
		return {'error': 'Not found'}
	
	cmd = request.values.get('cmd')
	if cmd == 'tags':
		new_tags = set(request.values.get('tags', '').split(','))
	
		cursor.execute('SELECT `tag` FROM `minutes_tags` WHERE `minutes_idx` = ?;', (idx,))
		tags = {row['tag'] for row in cursor.fetchall()}
	
		removed_tags = tags - new_tags
		added_tags = new_tags - tags
	
		for tag in removed_tags:
			cursor.execute('DELETE FROM `minutes_tags` WHERE `minutes_idx` = ? AND `tag` = ?;', (idx, tag))
	
		for tag in added_tags:
			cursor.execute('INSERT INTO `minutes_tags` VALUES (NULL, ?, ?);', (idx, tag))
	elif cmd == 'memo':
		memo = request.values.get('memo', '')
		cursor.execute('UPDATE `minutes` SET `memo` = ? WHERE `idx` = ?;', (memo, idx))
	
	conn.commit()
	return {'result': 'success'}

@app.route('/ajax/minutes', methods=['GET', 'POST', 'DELETE'])
@api_returns
def ajax_minutes():
	conn = get_db()
	cursor = conn.cursor()
	
	if request.method == 'DELETE':
		import os
		
		idx = request.values.get('idx')
		cursor.execute('SELECT filename FROM `minutes` WHERE `idx` = ?;', (idx,))
		row = cursor.fetchone()
		if row is None:
			return {'error': 'Not found'}
		
		fp = os.path.join(app.config.get('UPLOAD_DIR', 'upload'), row['filename'])
		if os.path.exists(fp):
			os.remove(fp)
		
		cursor.execute('DELETE FROM `minutes` WHERE `idx` = ?;', (idx,))
		conn.commit()
	
	# GET, DELETE
	cursor.execute('SELECT * FROM `minutes` WHERE 1 = 1;')
	result = cursor.fetchall()
	for row in result:
		make_row(row, cursor)
	
	return {'minutes': result}

@app.route('/ajax/upload', methods=['POST'])
@api_returns
def ajax_upload():
	import os, time
	
	file = request.files.get('file')
	if file is None or file.filename == '': return {'error': 'Bad request'}
	
	filename = '{}.mp4'.format(int(time.time()*1000))
	fp = os.path.join(app.config.get('UPLOAD_DIR', 'upload'), filename)
	file.save(fp)
	filesize = os.stat(fp).st_size
	
	conn = get_db()
	cursor = conn.cursor()
	cursor.execute('INSERT INTO `minutes` VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
		(file.filename, 0, 'pending', filename, filesize, int(time.time()), 0, '', ''))
	conn.commit()
	
	# status: pending, processing, error, done
	
	cursor.execute('SELECT * FROM `minutes` WHERE 1 = 1;')
	result = cursor.fetchall()
	for row in result:
		make_row(row, cursor)
	
	return {'minutes': result}
	#return {'result': 'success'}


##########################################################################################

@app.route('/robots.txt')
def robots_txt():
	return "User-agent: *\nDisallow: /"


'''

minutes

idx, name, status, filename, filesize, created_at, is_private, 

pending
processing
done


'''