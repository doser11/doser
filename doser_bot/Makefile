# Doser Makefile
# Quick commands for development

.PHONY: help install test clean run gui cli format lint

# Default target
help:
	@echo "Doser - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run GUI application"
	@echo "  make gui        - Run GUI application"
	@echo "  make cli        - Run CLI application"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean generated files"
	@echo "  make format     - Format code with black"
	@echo "  make lint       - Lint code with flake8"
	@echo ""

# Installation
install:
	pip install -r requirements.txt

# Run GUI
gui:
	python main.py

run: gui

# Run CLI
cli:
	python cli.py

# Run tests
test:
	python test_bot.py

# Clean generated files
clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf *.pyc
	rm -rf */*.pyc
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

# Format code (requires black)
format:
	black . --exclude venv/

# Lint code (requires flake8)
lint:
	flake8 . --exclude venv/ --max-line-length=100

# Setup development environment
dev-setup:
	python -m venv venv
	$(MAKE) install
	cp .env.example .env
	cp proxies.txt.example proxies.txt

# Build distribution
build:
	python setup.py sdist bdist_wheel

# Quick test with sample data
quick-test:
	@echo "Running quick test..."
	python -c "from utils.generators import DataGenerator; g = DataGenerator(); print(g.generate_complete_profile())"
