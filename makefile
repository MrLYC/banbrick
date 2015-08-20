ROOTPATH := .
DEVPATH = $(ROOTPATH)/.dev
DEVMKFILE := $(DEVPATH)/makefile
SRCPATH := $(ROOTPATH)/banbrick

# ENV VARS
PYENV := env PYTHONPATH=$(SRCPATH) DJANGO_SETTINGS_MODULE=banbrick.settings
PYTHON := $(PYENV) python
PEP8 := $(PYENV) pep8 --repeat --ignore=E202,E501
PYLINT := $(PYENV) pylint --disable=I0011 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
PYTEST := $(PYENV) py.test -v -x
DJMANAGE := $(PYENV) $(SRCPATH)/manage.py
PIPINSTALL := $(PYENV) pip install

-include $(DEVMKFILE)

.PHONY: dev-mk clean full-clean pylint pylint-full test requires compilemessages syncdb init demo-run

dev-mk:
	@echo "\033[33mmake from $(DEVMKFILE)\033[0m"

clean:
	@find . -name "__pycache__" -type d -exec rm -rf {} \; >/dev/null 2>&1 || true
	@find . -name "*.pyc" -type f -exec rm -rf {} \; >/dev/null 2>&1 || true
	@echo "\033[33mclean $(SRCPATH)\033[0m"

full-clean: clean
	@git clean -f
	@find $(SRCPATH) -name "migrations" -type d -exec rm -rf {}/ \; || true
	@rm db.sqlite3 || true

pylint:
	$(PEP8) $(SRCPATH)
	$(PYLINT) -E $(SRCPATH)

pylint-full:
	$(PYLINT) $(SRCPATH)

test: pylint
	$(PYTEST) $(SRCPATH)

requires: $(ROOTPATH)/requirements.txt
	$(PIPINSTALL) -r $(ROOTPATH)/requirements.txt

compilemessages:
	$(DJMANAGE) compilemessages_all

syncdb:
	$(DJMANAGE) makemigrations
	$(DJMANAGE) syncdb

init: requires syncdb compilemessages
	$(DJMANAGE) loaddata $(SRCPATH)/banbrick/fixture/initial_data.json

server-run:
	$(eval port ?= 9274)
	$(DJMANAGE) runserver 0:$(port)

demo-run: full-clean init
	$(eval port ?= 9274)
	make server-run port=$(port)
