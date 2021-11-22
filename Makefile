install:
	pipenv install

dev:
	pipenv install --dev

shell:
	pipenv shell

lint:
	black main.py
	black src/
