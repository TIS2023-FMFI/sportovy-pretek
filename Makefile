.PHONY: test install build

test:
	python -m unittest discover -v -s src/orienter/tester -t src/ -p "*_test.py"

install: dist/orienter-0.0.9-py3-none-any.whl
	pip install dist/orienter-0.0.9-py3-none-any.whl

build:
	python -m build

dist/orienter-0.0.9-py3-none-any.whl:
	python -m build