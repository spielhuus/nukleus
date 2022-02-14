VERSION=$(shell grep -Po 'version = \K(\d\.\d\.\d)' setup.cfg)
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MYPY = $(VENV)/bin/mypy
COVERAGE = $(VENV)/bin/coverage
SPHINX = $(VENV)/bin/sphinx-build

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = src/docs
BUILDDIR      = dist/doc

COVARAGE_SOURCES = src
CMD_COVERAGE_TEST = -m unittest discover -s src/test
CMD_COVERAGE_RUN = $(COVERAGE) run --append --source $(COVARAGE_SOURCES) $(CMD_COVERAGE_TEST)
TARGET=dist/nukleus-$(VERSION)-py3-none-any.whl

.PHONY: help test doc clean pyre Makefile

all: $(TARGET)

$(TARGET): $(VENV)/bin/activate
	$(PYTHON) -m build

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

test: $(VENV)/bin/activate
	$(PYTHON) -m unittest discover -s src/test

coverage: $(VENV)/bin/activate
	$(CMD_COVERAGE_RUN)
	$(COVERAGE) report -m

mypy: 
	 $(MYPY) src


install: $(TARGET)
	$(PIP) install $(TARGET)

clean:
	rm -rf dist
	rm -rf `find src -name __pycache__`
	rm -rf src/nukleus.egg-info
	rm -rf $(VENV)


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
doc:
	$(SPHINX) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
