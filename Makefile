
run:
	export DJANGO_SETTINGS_MODULE=blogs_django.settings
	poetry run gunicorn blogs_django.wsgi

run-test:
	poetry run python manage.py runserver