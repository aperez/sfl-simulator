.PHONY: run plot

ENV = env
PYTHON = $(ENV)/bin/python3
#PFLAGS = -m cProfile -s cumtime
PFLAGS =
PIP = $(ENV)/bin/pip3

run: $(ENV)
	mkdir -p output
	mkdir -p tmp
	$(PYTHON) $(PFLAGS) run.py --sim

plot: $(ENV)
	$(PYTHON) $(PFLAGS) run.py --plot

$(ENV): $(ENV)/bin/activate

$(ENV)/bin/activate: requirements.txt
	python3 -m venv $(ENV)
	$(PIP) install -Ur requirements.txt
