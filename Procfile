release: python manage.py migrate
web: daphne final_project_app.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=final_project_app.settings -v2