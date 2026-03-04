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

# Run the project
run:
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: No config .txt file found."; \
	fi
	python3 $(MAIN) $(CONFIG)

debug:
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: No config .txt file found."; \
	fi
	python3 -m pdb a_maze_ing.py $(CONFIG)

# Lint code (requires flake8)
lint:
	$(PYTHON) -m flake8 .

# Clean python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Rebuild everything
re: clean

.PHONY: all run lint clean re

