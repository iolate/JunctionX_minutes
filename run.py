import os
os.environ['APP_SETTINGS'] = 'settings.cfg'

from flask_app import app

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
