#!/bin/bash

# Constants
REPO_URL="https://github.com/judithkwesi/ip-monitoring-tool.git"
PROJECT_DIR="/Users/charleskasasira/Documents/Development/Intern/RENU/team1/ip-monitoring-tool"
VENV_DIR="/Users/charleskasasira/Documents/Development/Intern/RENU/team1/env"
# SYSTEMD_SERVICE="your_service_name.service"

# Function to update the code from GitHub
update_code() {
    echo "Updating code from GitHub..."
    git pull origin staging
}

# Function to install Python dependencies
install_dependencies() {
    echo "Installing Python dependencies..."
    cd "$PROJECT_DIR"
    echo "Activating Virtual Environment..."
    source $VENV_DIR/bin/activate
    pip install -r requirements.txt
}

# Function to run database migrations
run_migrations() {
    echo "Running database migrations..."
    cd "$PROJECT_DIR"
    source $VENV_DIR/bin/activate
    echo "Activating Virtual Environment..."
    python manage.py migrate
}

run_collectstatic() {
    echo "Running static files..."
    cd "$PROJECT_DIR"
    source $VENV_DIR/bin/activate
    echo "Activating Virtual Environment..."
    python manage.py collectstatic
}

# Function to restart the server
# restart_server() {
#     echo "Restarting the server..."
#     sudo systemctl restart $SYSTEMD_SERVICE
# }

# Main deployment process
main() {
    update_code
    install_dependencies
    run_migrations
    # restart_server
    # run_collectstatic
    echo "Deployment successful!"
}

main
