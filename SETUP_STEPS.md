# Pipetrace Setup Steps

This document outlines the complete process to recreate this repository from scratch.

## Initial Setup

1. Create the repository and initialize git:
   ```bash
   mkdir pipetrace
   cd pipetrace
   git init
   ```

2. Create core org-mode files:
   ```bash
   # Create setup.org with source code blocks for:
   # - src/pipetrace.py (core tracing functionality)
   # - src/example.py (example usage)
   # - src/read_fifo.py (FIFO reader utility)
   ```

3. Add Makefile with basic targets:
   ```bash
   # Create Makefile with targets for:
   # - help: Show available commands
   # - run: Run the example script
   # - monitor: Run the FIFO monitor
   # - fifo: Create the FIFO if it doesn't exist
   # - tangle: Tangle org files with Emacs
   # - clean: Remove generated files
   ```

4. Create README.org with project documentation:
   ```bash
   # Create README.org with:
   # - Project overview
   # - Features
   # - Quick start guide
   # - Architecture diagram
   # - Usage examples
   ```

5. Tangle the org files to generate source code:
   ```bash
   # Either use emacs directly:
   emacs --batch --eval "(progn (find-file \"setup.org\") (org-babel-tangle) (find-file \"setup-v2.org\") (org-babel-tangle))"
   
   # Or use the Makefile:
   make tangle
   ```

## Package Structure

1. Create Python package structure:
   ```bash
   mkdir -p src/pipetrace
   touch src/pipetrace/__init__.py
   
   # Copy source files to package directory
   cp src/pipetrace.py src/pipetrace/
   cp src/read_fifo.py src/pipetrace/
   ```

2. Create pyproject.toml:
   ```bash
   cat > pyproject.toml << EOF
   [build-system]
   requires = ["setuptools>=61.0", "wheel"]
   build-backend = "setuptools.build_meta"
   
   [project]
   name = "pipetrace"
   version = "0.1.0"
   description = "A lightweight Python tool for tracing program control flow using named pipes (FIFOs)"
   readme = "README.md"
   requires-python = ">=3.6"
   license = {text = "MIT"}
   authors = [
       {name = "jwalsh", email = "example@example.com"}
   ]
   # ... additional metadata ...
   EOF
   ```

3. Update Makefile for package management:
   ```bash
   # Add targets for:
   # - README.md: Convert README.org to markdown
   # - setup: Set up development environment
   # - install: Install the package
   ```

4. Set Python version:
   ```bash
   echo "3.11" > .python-version
   ```

## Development Environment

1. Create direnv configuration:
   ```bash
   cat > .envrc << EOF
   #!/bin/sh
   # direnv configuration for pipetrace
   
   # Setup the environment using make
   make -s setup
   
   # Activate the virtual environment if it exists
   if [ -d .venv ]; then
       source .venv/bin/activate
       export PYTHONPATH="$PWD:$PYTHONPATH"
       echo "✅ Pipetrace development environment activated"
   fi
   EOF
   ```

2. Update .gitignore:
   ```bash
   cat > .gitignore << EOF
   # Python
   __pycache__/
   *.py[cod]
   .venv/
   
   # Generated files
   README.md
   
   # Project-specific files to exclude
   # ...
   EOF
   ```

## Verify Installation

1. Setup the environment:
   ```bash
   make setup
   ```

2. Test the example:
   ```bash
   # Run the example in one terminal
   make run
   
   # Run the monitor in another terminal
   make monitor
   ```

3. Try the dashboard:
   ```bash
   make demo
   ```

## Create GitHub Repository

1. Create the repository:
   ```bash
   gh repo create pipetrace --public
   ```

2. Add description and topics:
   ```bash
   gh repo edit pipetrace --description "A lightweight Python tool for tracing program control flow using named pipes (FIFOs)" --add-topic python,debugging,tracing,control-flow,fifo,named-pipes,monitoring
   ```

3. Push the repository:
   ```bash
   git remote add origin https://github.com/username/pipetrace.git
   git push -u origin main
   ```

## Final Testing

1. Clone the repository fresh:
   ```bash
   cd /tmp
   git clone https://github.com/username/pipetrace.git
   cd pipetrace
   ```

2. Setup and test:
   ```bash
   make setup
   make demo
   ```