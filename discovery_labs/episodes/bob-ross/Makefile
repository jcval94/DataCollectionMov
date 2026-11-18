.PHONY: check research clusters all
PYTHON ?= python
check:
	$(PYTHON) run.py --check
	$(PYTHON) -m unittest discover -s tests -v
research:
	$(PYTHON) run.py --write
clusters:
	$(PYTHON) clustering.py --write
all: check research clusters
