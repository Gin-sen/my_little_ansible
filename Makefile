# Makefile for your python environement
#
#
#
SHELL := /bin/bash
.ONESHELL:

EXEC	=	venv/bin/mla
SRC	=	$(wildcard *.py)
OBJ	=	$(SRC:.py=.pyc)



venv: venv/touchfile

venv/touchfile:
	python3.10 -m venv venv
	@touch venv/touchfile
	@source ./venv/bin/activate

install:	requirements.txt
	./venv/bin/pip3.10 install -r requirements.txt


build:
	./venv/bin/pip3.10 install .

run:	venv/touchfile install build
	./venv/bin/mla

clean:
	@rm -rf .pytest_cache/ .cache/ build/ dist/ ./__pycache__

fclean:	clean
	@rm -rf ./venv/bin/mla

help:
	@cat Makefile