import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.environ['APP_SETTINGS'] = 'settings.cfg'

from flask_app import app

if __name__ == '__main__':
    app.run()

# sudo gunicorn -k eventlet -w 1 -b unix:/tmp/wsgi.sock -m 007 -u ubuntu -g www-data wsgi:app
# sudo gunicorn -k eventlet -w 2 --threads 2 -b 0.0.0.0:8000 wsgi:app
