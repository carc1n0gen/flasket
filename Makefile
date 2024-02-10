all: setup dev


setup:
	test -d .venv || python -m venv .venv
	. .venv/bin/activate; pip install -r requirements.txt


dev:
	. .venv/bin/activate; flask run --debug


build:
	. .venv/bin/activate; flask freeze


clean:
	rm -rf .venv
	rm -rf build