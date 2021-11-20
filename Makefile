
run:
	export DJANGO_SETTINGS_MODULE=blogs_django.settings
	poetry run gunicorn blogs_django.wsgi

run-test:
	poetry run python manage.py runserver

test:
	poetry run python manage.py test tests/

console:
	poetry run python manage.py shell

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate