.PHONY: install install-dev lint format test test-cov clean build build-exe

install:
	poetry install

install-dev:
	poetry install --with dev

lint:
	poetry run ruff check src/ tests/
	poetry run mypy src/

format:
	poetry run black src/ tests/
	poetry run ruff check --fix src/ tests/

test:
	poetry run pytest tests/

test-cov:
	poetry run pytest --cov=reportgen --cov-report=html tests/

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .mypy_cache
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	poetry run python -m build

build-exe:
	poetry run pyinstaller --clean --onefile --name nessus-reportgen src/reportgen/cli.py

build-exe-spec:
	poetry run pyinstaller --clean nessus-reportgen.spec
