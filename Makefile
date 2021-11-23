install:
	pipenv install

dev:
	pipenv install --dev

shell:
	pipenv shell

lint:
	pipenv run black main.py
	pipenv run black src/
