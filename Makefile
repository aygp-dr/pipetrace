# Pipetrace Makefile

.PHONY: all clean run monitor test tangle help setup demo watch version install

# Default target
all: fifo run

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
	@echo "  setup    : Set up development environment"
	@echo "  demo     : Run a complete demo in tmux"
	@echo "  watch    : Monitor for changes and rerun"
	@echo "  version  : Show version information"
	@echo "  install  : Install as a package"
	@echo "  all      : Run fifo and example script"
	@echo "  help     : Show this help message"
	@echo ""
	@echo "Usage examples:"
	@echo "  make run      # Run the example script"
	@echo "  make monitor  # In another terminal, monitor the FIFO"
	@echo "  make demo     # Run a complete demo in tmux"

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

# Setup development environment
setup:
	@echo "Setting up development environment..."
	@uv init || echo "Project already initialized"
	@uv venv
	@echo "Environment ready! Activate with: source .venv/bin/activate"

# Run a complete demo in tmux
demo:
	@echo "Starting pipetrace demo in tmux..."
	tmux new-session -s pipetrace -d || (tmux kill-session -t pipetrace && tmux new-session -s pipetrace -d)
	tmux split-window -h -t pipetrace
	tmux send-keys -t pipetrace:0.1 'make monitor' C-m
	tmux send-keys -t pipetrace:0.0 'sleep 1 && make run' C-m
	tmux attach -t pipetrace

# Watch for changes and rerun
watch:
	@echo "Watching for changes and rerunning..."
	@while true; do \
		make fifo; \
		make run; \
		sleep 5; \
	done

# Show version information
version:
	@echo "Pipetrace Version: 0.1.0"
	@python --version
	@uv --version
	@uname -a

# Install as a package
install:
	@echo "Installing pipetrace..."
	@mkdir -p ~/.local/bin
	@cp src/pipetrace.py ~/.local/bin/pipetrace
	@chmod +x ~/.local/bin/pipetrace
	@echo "Installed pipetrace to ~/.local/bin/pipetrace"
	@echo "Make sure ~/.local/bin is in your PATH"