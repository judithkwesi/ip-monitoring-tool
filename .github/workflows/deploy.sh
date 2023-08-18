#!/bin/bash

# Constants
REPO_URL="https://github.com/judithkwesi/ip-monitoring-tool.git"
PROJECT_DIR="/home/ssenabulyadavid/ip-monitoring-tool/ip-monitoring-tool"
VENV_DIR="/home/ssenabulyadavid/ip-monitoring-tool/env"
SYSTEMD_SERVICE="ip-monitoring-tool.service"

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
    python manage.py makemigrations mainapp
    python manage.py migrate
}

run_collectstatic() {
    echo "Running static files..."
    cd "$PROJECT_DIR"
    source $VENV_DIR/bin/activate
    echo "Activating Virtual Environment..."
    chmod +w "$PROJECT_DIR"/static
    python manage.py collectstatic --noinput
}

# Function to restart the server
restart_server() {
    echo "Restarting the server..."
    sudo systemctl restart $SYSTEMD_SERVICE
}

# Main deployment process
main() {
    update_code
    # install_dependencies
    run_migrations
    run_collectstatic
    restart_server
    echo "Deployment successful!"
}

main
