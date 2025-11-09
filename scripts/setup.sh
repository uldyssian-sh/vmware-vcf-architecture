#!/bin/bash
# VMware VCF Architecture - Setup Script
# This script sets up the development environment

set -euo pipefail

echo "🚀 Setting up VMware VCF Architecture development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Create .env file from template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.template .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Run initial tests
echo "🧪 Running initial tests..."
pytest tests/ -v

# Run security checks
echo "🔒 Running security checks..."
bandit -r . -f json -o bandit-report.json || true

echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'source venv/bin/activate' to activate the virtual environment"
echo "3. Run 'python main.py --health-check' to verify installation"
echo "4. Run 'make help' to see available commands"# Updated Sun Nov  9 12:49:47 CET 2025
# Updated Sun Nov  9 12:52:31 CET 2025
# Updated Sun Nov  9 12:56:20 CET 2025
