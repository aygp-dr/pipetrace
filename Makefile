# Pipetrace Makefile

.PHONY: all clean run monitor test tangle help

# Default target
all: help

# Help message
help:
	@echo "Pipetrace Makefile"
	@echo "=================="
	@echo ""
	@echo "Available targets:"
	@echo "  run      : Run the example script"
	@echo "  monitor  : Run the FIFO monitor"
	@echo "  fifo     : Create the FIFO if it doesn't exist"
	@echo "  tangle   : Tangle org files with Emacs"
	@echo "  clean    : Remove generated files"
	@echo "  test     : Run tests"
	@echo "  help     : Show this help message"
	@echo ""
	@echo "Usage examples:"
	@echo "  make run      # Run the example script"
	@echo "  make monitor  # In another terminal, monitor the FIFO"

# Run the example script
run: fifo
	python src/example.py

# Run the FIFO monitor
monitor: fifo
	python src/read_fifo.py

# Create the FIFO
fifo:
	python -c "import os; os.mkfifo('/tmp/pipetrace_fifo') if not os.path.exists('/tmp/pipetrace_fifo') else print('FIFO already exists')"

# Tangle org files
tangle:
	emacs --batch --eval "(progn (find-file \"setup.org\") (org-babel-tangle) (find-file \"setup-v2.org\") (org-babel-tangle))"

# Clean generated files
clean:
	python -c "import os, shutil; shutil.rmtree('__pycache__', ignore_errors=True); shutil.rmtree('src/__pycache__', ignore_errors=True); os.unlink('/tmp/pipetrace_fifo') if os.path.exists('/tmp/pipetrace_fifo') else None"
	@echo "Cleaned up generated files"

# Run tests (placeholder for future tests)
test:
	@echo "No tests implemented yet"