.PHONY: test build

test:
	python -m unittest discover -s src/orienter/tester -t src/ -p "*_test.py"

build:
	python -m build