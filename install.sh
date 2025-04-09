#!/bin/bash

# PYTHON ENVIRONMENT INSTALLATION SCRIPT
# Create a virtual environment in the "venv" folder
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "The virtual environment 'venv' already exists."
fi

# Activate the virtual environment
if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    # For Linux/macOS
    source .venv/bin/activate
elif [ "$(uname)" == "CYGWIN"* ] || [ "$(uname)" == "MINGW"* ] || [ "$(uname)" == "MSYS"* ]; then
    # For Windows
    source .venv/Scripts/activate
else
    echo "System unrecognized. Please activate the virtual environment manually."
    exit 1
fi

# Install required Python packages
pip install PyQt5 mysql-connector-python

echo "Packages PyQt5 and mysql-connector-python installed."



# MYSQL INSTALLATION SCRIPT
echo "Installing MySQL..."

# Linux package management detection
if [ -f /etc/os-release ]; then
    # Debian/Ubuntu-based
    if grep -iq "ubuntu" /etc/os-release || grep -iq "debian" /etc/os-release || grep -iq "kali" /etc/os-release; then
        sudo apt-get install -y mysql-server
        sudo systemctl start mysql
        sudo systemctl enable mysql
        echo "MySQL installed and started (Ubuntu/Debian)."
    # Arch Linux-based
    elif grep -iq "arch" /etc/os-release || grep -iq "manjaro" /etc/os-release; then
        sudo pacman -S --noconfirm mysql
        sudo systemctl start mysqld
        sudo systemctl enable mysqld
        echo "MySQL installed and started (Arch Linux)."
    # Fedora-based
    elif grep -iq "fedora" /etc/os-release; then
        sudo dnf install -y mysql-server
        sudo systemctl start mysqld
        sudo systemctl enable mysqld
        echo "MySQL installed and started (Fedora)."
    else
        echo "Unknown Linux distribution. Please install MySQL manually."
        exit 1
    fi
elif [ "$(uname)" == "Darwin" ]; then
    # For macOS
    if command -v brew &> /dev/null; then
        brew install mysql
        brew services start mysql
        echo "MySQL installed and started (macOS with Homebrew)."
    else
        echo "Homebrew is required for MySQL installation on macOS."
        exit 1
    fi
else
    echo "MySQL installation skipped (not supported OS). Please install MySQL manually."
    exit 1
fi

# Create a MySQL user and assign privileges
echo "Creating MySQL user 'rootuser'..."
sudo mysql -e "CREATE USER 'rootuser'@'localhost' IDENTIFIED BY 'rootuser';"
sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'rootuser'@'localhost' WITH GRANT OPTION;"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "User 'rootuser' created with privileges."


# INSTALLATION COMPLETE
echo
echo "######################################################################################################"
echo
echo "The installation is complete."
echo
echo "Please run the following command to activate the virtual environment for Python using Linux/macOS:"
echo "source .venv/bin/activate"
echo
echo "For Windows, use the following command:"
echo "source .venv/Scripts/activate"
echo
echo "To run the program, use the following command:"
echo "python3 main.py"