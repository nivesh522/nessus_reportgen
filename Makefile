.PHONY: install install-dev lint format test test-cov clean build build-exe

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

test:
	pytest tests/

test-cov:
	pytest --cov=reportgen --cov-report=html tests/

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf *.spec
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python3 -m build

build-exe:
	pyinstaller --clean --onefile --name nessus-reportgen src/reportgen/cli.py

build-exe-spec:
	pyinstaller --clean nessus-reportgen.spec
