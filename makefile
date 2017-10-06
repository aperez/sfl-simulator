.PHONY: run

ENV = env
PYTHON = $(ENV)/bin/python3
#PFLAGS = -m cProfile -s cumtime
PFLAGS =
PIP = $(ENV)/bin/pip3

run: $(ENV)
	mkdir output
	$(PYTHON) $(PFLAGS) run.py

$(ENV): $(ENV)/bin/activate

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(PIP) install -Ur requirements.txt
