run:
	ENV=production gunicorn app:app \
		--error-logfile - \
		-b 0.0.0.0:8080