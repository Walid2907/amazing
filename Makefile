# ==========================
# Python Project Makefile
# Project: a-maze-ing.py
# ==========================

PYTHON = python3
MAIN = a-maze-ing.py
VENV = venv
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python

# Default target
all: run

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV)

# Install dependencies
install: venv
	$(PIP) install -r requirements.txt

# Run the project
run:
	$(PYTHON) $(MAIN)

# Run using virtual environment python
run-venv: venv
	$(PY) $(MAIN)

# Format code (requires black)
format:
	$(PYTHON) -m black .

# Lint code (requires flake8)
lint:
	$(PYTHON) -m flake8 .

# Clean python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Remove virtual environment
fclean: clean
	rm -rf $(VENV)

# Rebuild everything
re: fclean install

.PHONY: all venv install run run-venv format lint clean fclean re
