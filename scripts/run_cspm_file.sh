#!/bin/bash

# Script to run CSPM (Cloud Security Posture Management) Python scripts
# with proper environment setup and dependency installation

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to display usage
usage() {
    echo "Usage: $0 <python_script> [script_args...]"
    echo ""
    echo "Run a CSPM Python script with virtual environment and dependency management."
    echo ""
    echo "Arguments:"
    echo "  python_script    Path to the Python script to execute"
    echo "  script_args      Optional arguments to pass to the Python script"
    echo ""
    echo "Environment:"
    echo "  - Loads .env file if present in current directory"
    echo "  - Activates virtual environment from ../.venv"
    echo "  - Installs dependencies from requirements.txt using Tsinghua mirror"
    echo ""
    exit 1
}

# Check if python_script argument is provided
if [ $# -eq 0 ]; then
    print_error "No Python script specified"
    echo ""
    usage
fi

PYTHON_SCRIPT="$1"
shift  # Remove first argument, remaining are script arguments
# Remaining arguments are stored in $@ array

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_info "Project root: $PROJECT_ROOT"
print_info "Python script: $PYTHON_SCRIPT"
if [ $# -gt 0 ]; then
    print_info "Script arguments:"
    for arg in "$@"; do
        print_info "  - '$arg'"
    done
fi

# 1. Load environment variables from .env file if it exists
ENV_FILE="$PROJECT_ROOT/.env"
if [ -f "$ENV_FILE" ]; then
    print_info "Loading environment variables from $ENV_FILE"
    # Use export to set variables (simple approach, doesn't handle multiline or quotes)
    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Skip comments and empty lines
        if [[ $key =~ ^# ]] || [[ -z "$key" ]]; then
            continue
        fi
        # Remove leading/trailing whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        export "$key=$value"
        print_info "  Set $key"
    done < "$ENV_FILE"
else
    print_warning "No .env file found at $ENV_FILE"
fi

# 2. Activate virtual environment
VENV_DIR="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
    print_error "Virtual environment not found at $VENV_DIR"
    print_error "Please create it with: python -m venv .venv"
    exit 1
fi

# Check for activate script (platform-specific)
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    # Windows
    ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
elif [ -f "$VENV_DIR/bin/activate" ]; then
    # Linux/Mac
    ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
else
    print_error "Could not find activate script in $VENV_DIR"
    exit 1
fi

print_info "Activating virtual environment: $ACTIVATE_SCRIPT"
source "$ACTIVATE_SCRIPT"

# Check if Python is available in virtual environment
if ! command -v python > /dev/null 2>&1; then
    print_error "Python not found in virtual environment"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1)
print_info "Using $PYTHON_VERSION"

# 3. Install dependencies from requirement.txt/requirements.txt using Tsinghua mirror
# Check for requirement files in multiple locations
REQUIREMENTS_FILE=""
if [ -f "requirement.txt" ]; then
    REQUIREMENTS_FILE="requirement.txt"
    print_info "Found requirement.txt in current directory"
elif [ -f "$SCRIPT_DIR/requirement.txt" ]; then
    REQUIREMENTS_FILE="$SCRIPT_DIR/requirement.txt"
    print_info "Found requirement.txt in scripts directory"
elif [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"
    print_info "Found requirements.txt in project root"
elif [ -f "$PROJECT_ROOT/requirement.txt" ]; then
    REQUIREMENTS_FILE="$PROJECT_ROOT/requirement.txt"
    print_info "Found requirement.txt in project root"
fi

if [ -n "$REQUIREMENTS_FILE" ] && [ -f "$REQUIREMENTS_FILE" ]; then
    print_info "Installing dependencies from $REQUIREMENTS_FILE"
    print_info "Using Tsinghua mirror: https://pypi.tuna.tsinghua.edu.cn/simple"

    # Upgrade pip first
    python -m pip install --upgrade pip

    # Install dependencies with mirror
    python -m pip install -r "$REQUIREMENTS_FILE" -i https://pypi.tuna.tsinghua.edu.cn/simple
else
    print_warning "No requirement.txt or requirements.txt found"
    print_warning "Skipping dependency installation"
fi

# 4. Run the Python script
print_info "Running Python script: $PYTHON_SCRIPT"
if [ ! -f "$PYTHON_SCRIPT" ]; then
    print_error "Python script not found: $PYTHON_SCRIPT"
    exit 1
fi

# Check if script is absolute path or relative
if [[ "$PYTHON_SCRIPT" != /* ]] && [[ "$PYTHON_SCRIPT" != ~* ]] && [[ "$PYTHON_SCRIPT" != .* ]]; then
    # Assume it's relative to current directory
    PYTHON_SCRIPT="./$PYTHON_SCRIPT"
fi

# Build command string for display
CMD_STR="python \"$PYTHON_SCRIPT\""
for arg in "$@"; do
    CMD_STR="$CMD_STR \"$arg\""
done
print_info "Executing: $CMD_STR"
echo "========================================================================"

# Run the script
python "$PYTHON_SCRIPT" "$@"

EXIT_CODE=$?
echo "========================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    print_info "Script completed successfully"
else
    print_error "Script failed with exit code: $EXIT_CODE"
fi

exit $EXIT_CODE

