#!/usr/bin/env bash
set -e

echo "Running AI OS Architecture Governance Layers..."

echo "====================="
echo "1. Running Semgrep..."
echo "====================="
semgrep ci --config .semgrep/rules.yaml || semgrep scan --config .semgrep/rules.yaml --error

echo "====================="
echo "2. Running Ruff..."
echo "====================="
ruff check .

echo "====================="
echo "3. Running ESLint..."
echo "====================="
npx eslint .

echo "====================="
echo "4. Running Unit Tests..."
echo "====================="
if command -v pytest &> /dev/null; then
    echo "Running Python tests with pytest..."
    pytest
else
    echo "pytest not found, skipping Python tests."
fi

if [ -f "package.json" ]; then
    echo "Running JS/TS tests with npm test..."
    npm test --passWithNoTests
else
    echo "package.json not found, skipping JS/TS tests."
fi

echo "====================="
echo "All gates passed successfully!"
echo "====================="
