#!/bin/bash

# Test runner for code-nautilus installation script tests
# This script runs all tests and provides a summary

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Code-Nautilus Installation Script Test Runner${NC}"
echo "=============================================="
echo ""

# Check if install.sh exists
if [ -f "install.sh" ]; then
    # Running from project root
    cp install.sh tests/
    cd tests
elif [ -f "../install.sh" ]; then
    # Running from tests directory
    cp ../install.sh .
else
    echo -e "${RED}Error: install.sh not found${NC}"
    echo "Please run this script from the project root or tests/ directory"
    exit 1
fi

echo -e "${YELLOW}Running installation script tests...${NC}"
echo ""

# Run the test suite
if ./test_install.sh; then
    echo ""
    echo -e "${GREEN}✓ All installation script tests passed!${NC}"
    exit_code=0
else
    echo ""
    echo -e "${RED}✗ Some installation script tests failed!${NC}"
    exit_code=1
fi

# Cleanup
rm -f install.sh

# Return to original directory if we changed it
if [ -f "../install.sh" ]; then
    cd ..
fi

exit $exit_code