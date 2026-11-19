.PHONY: check research clusters browser-qa all
PYTHON ?= python
check:
	$(PYTHON) run.py --check
	$(PYTHON) -m unittest discover -s tests -v
research:
	$(PYTHON) run.py --write
clusters:
	$(PYTHON) clustering.py --write
all: check research clusters

browser-qa:
	node qa_static.cjs
