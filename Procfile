tasks: celery -A shield worker --pool=solo -B -l info
release: python manage.py migrate
release: python manage.py collectstatic
web: gunicorn shield.wsgi --log-file -
