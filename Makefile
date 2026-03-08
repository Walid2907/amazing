# ==========================
# Python Project Makefile
# Project: a-maze-ing.py
# ==========================

PYTHON = python3
MAIN = a_maze_ing.py

# Default target
all: run

CONFIG ?= $(shell find . -maxdepth 1 -name "*.txt" ! -name "maze.txt" | head -1)
CONFIG := $(if $(CONFIG),$(CONFIG),config.txt)

# Install project dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt

# Run the project
run:
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: No config .txt file found."; \
	fi
	$(PYTHON) $(MAIN) $(CONFIG)

# Debug mode
debug:
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: No config .txt file found."; \
	fi
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Lint code
lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Strict lint (optional/recommended)
lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

# Clean python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Rebuild everything
re: clean

.PHONY: all install run debug lint lint-strict clean re