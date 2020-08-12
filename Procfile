tasks: celery -A shield worker --pool=solo -B -l info
release: python manage.py migrate
web: gunicorn shield.wsgi --log-file -
