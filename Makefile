# Makefile for your python environement
#
#
#
EXEC	=	venv/bin/mla
SRC	=	$(wildcard *.py)
OBJ	=	$(SRC:.py=.pyc)



venv/bin/mla:	requirements.txt
	./venv/bin/pip3.10 install -r requirements.txt
	./venv/bin/python3.10 -m pip install .

venv/bin/activate:	requirements.txt
	python3.10 -m venv venv
	./venv/bin/pip3.10 install -r requirements.txt
	echo "!!!!!! USE \"source ./venv/bin/activate\" !!!!!!"

run:	venv/bin/activate venv/bin/mla
	./venv/bin/pip3.10 install .
	./venv/bin/mla

clean:
	@rm -rf .pytest_cache/ .cache/ build/ dist/ ./venv/bin/mla

fclean:	clean
	@rm -rf ./venv/bin/mla

help:
	@cat Makefile