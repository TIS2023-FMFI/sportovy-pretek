.PHONY: test build

test:
	python -m unittest discover -v -s src/orienter/tester -t src/ -p "*_test.py"

build:
	python -m build