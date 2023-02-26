# flask --app craui --debug run --port 7007

gunicorn --workers 4 --bind 0.0.0.0:7007 'craui:create_app()'