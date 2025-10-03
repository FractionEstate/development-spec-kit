#!/usr/bin/env bash
# Deployment Validation Script
# Runs all checks before production deployment

echo "============================================"
echo "  Specify CLI - Deployment Validation"
echo "============================================"
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0

# Function to run a test
run_test() {
    local name="$1"
    local command="$2"

    echo -n "Testing: $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC}"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# 1. Code Quality Checks
echo "📋 Code Quality"
echo "---"
run_test "Markdown linting" "markdownlint-cli2 README.md CHANGELOG.md"
run_test "Python files present" "test -f src/specify_cli/__init__.py"
echo

# 2. CLI Functionality
echo "🔧 CLI Functionality"
echo "---"
run_test "specify version" "specify version"
run_test "specify --help" "specify --help"
run_test "specify list-models" "specify list-models | grep -q gpt-4o"
run_test "specify check" "specify check"
echo

# 3. Model Catalog
echo "📦 Model Catalog"
echo "---"
run_test "Has 50+ models" "test $(specify list-models | wc -l) -gt 50"
run_test "Includes Claude" "specify list-models | grep -qi claude"
run_test "Includes GPT-4o" "specify list-models | grep -q gpt-4o"
run_test "Includes Claude Sonnet 4.5" "specify list-models | grep -q 'claude-sonnet-4.5'"
echo

# 4. Documentation
echo "📚 Documentation"
echo "---"
run_test "README.md exists" "test -f README.md"
run_test "CHANGELOG.md exists" "test -f CHANGELOG.md"
run_test "AGENTS.md exists" "test -f AGENTS.md"
run_test "docs/ directory" "test -d docs"
run_test "tests/ directory" "test -d tests"
echo

# 5. Package Building
echo "📦 Package Building"
echo "---"
run_test "uv build succeeds" "uv build"
run_test "Wheel file created" "test -f dist/*.whl"
run_test "Source distribution" "test -f dist/*.tar.gz"
echo

# 6. CI/CD Workflows
echo "⚙️  CI/CD Workflows"
echo "---"
run_test "lint.yml exists" "test -f .github/workflows/lint.yml"
run_test "test.yml exists" "test -f .github/workflows/test.yml"
run_test "build.yml exists" "test -f .github/workflows/build.yml"
run_test "security.yml exists" "test -f .github/workflows/security.yml"
echo

# 7. Tests
echo "🧪 Test Suite"
echo "---"
run_test "pytest runs" "pytest tests/ -q"
echo

# Summary
echo "============================================"
echo "  Deployment Validation Summary"
echo "============================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix before deploying.${NC}"
    exit 1
fi
