VERSION=$(shell grep -Po 'version = \K(\d\.\d\.\d)' setup.cfg)
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
PYRIGHT = $(VENV)/bin/pyright
COVERAGE = $(VENV)/bin/coverage
SPHINX = $(VENV)/bin/sphinx-build
PCBNEW := $(shell find /usr/lib -name pcbnew.py)
PCBNEWSO := $(shell find /usr/lib -name _pcbnew.so)
PYVERSION := $(shell python3 --version|sed 's/.* \([0-9]\.[0-9]*\).*/\1/')

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

SOURCES = $(wildcard src/nukleus/*.py) $(wildcard src/nukleus/**/*.py)

all: $(TARGET)

$(TARGET): $(VENV)/bin/activate $(SOURCES)
	$(PYTHON) -m build

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	$(info '$(PCBNEW)')
	@[ -z "${PCBNEW}" ] && (echo "not linking pcbnew") || ln -s $(PCBNEW) $(VENV)/lib/python$(PYVERSION)/site-packages/pcbnew.py
	@[ -z "${PCBNEWSO}" ] && (echo "not linking pcbnew") || ln -s $(PCBNEWSO) $(VENV)/lib/python$(PYVERSION)/site-packages/_pcbnew.so


test: $(VENV)/bin/activate
	$(PYTHON) -m unittest discover -s src/test

coverage: $(VENV)/bin/activate
	$(CMD_COVERAGE_RUN)
	$(COVERAGE) report -m

type: 
#	 $(PYRIGHT) $(SOURCES)
	 $(PYTHON) -m pyright $(SOURCES)


install: $(TARGET)
	$(PIP) install --force $(TARGET)

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
