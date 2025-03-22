#!/bin/bash

echo "==================================="
echo "Recipe Genie - Installation Script"
echo "==================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH."
    echo "Please install Python 3.8 or higher."
    echo "On Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "On macOS: brew install python"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    echo "Please make sure you have venv module installed."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

# Create launch script
echo "Creating launch script..."
cat > run_recipe_genie.sh << 'EOF'
#!/bin/bash
source .venv/bin/activate
python3 main.py
EOF

chmod +x run_recipe_genie.sh

echo
echo "==================================="
echo "Installation complete!"
echo
echo "To start Recipe Genie, run: ./run_recipe_genie.sh"
echo
echo "Before using, make sure to update config.json with your API key."
echo "==================================="
echo
