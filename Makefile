.PHONY: test install build

test:
	python -m unittest discover -v -s src/orienter/tester -t src/ -p "*_test.py"

install:
	pip install dist/orienter-0.0.8-py3-none-any.whl

build:
	python -m build