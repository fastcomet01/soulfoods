#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run test suite
if pytest test_soul_foods.py -v; then
    echo "All tests passed."
    exit 0
else
    echo "One or more tests failed."
    exit 1
fi
