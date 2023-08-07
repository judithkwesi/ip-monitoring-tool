#!/bin/bash

# Constants
REPO_URL="https://github.com/judithkwesi/ip-monitoring-tool.git"
PROJECT_DIR="/home/charles/ip-reputation/staging/ip-monitoring-tool"
VENV_DIR="/home/charles/ip-reputation/staging/dev_env"
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
    chmod +w "$PROJECT_DIR"/static


    python manage.py collectstatic --noinput
}

# Function to restart the server
# restart_server() {
#     echo "Restarting the server..."
#     sudo systemctl restart $SYSTEMD_SERVICE
# }

# Function to stop the program running on port 8001
stop_program_on_port() {
    echo "Stopping program on port 8001..."
    local pids=$(sudo lsof -t -i :8001)

    if [ -z "$pids" ]; then
        echo "No program found running on port 8001."
    else
        for pid in $pids; do
            sudo kill -9 "$pid"
            echo "Terminated process with PID: $pid"
        done
        echo "Program(s) stopped successfully."
    fi

    # restart gunicorn
    gunicorn ip-monitoring-tool.wsgi:application --bind 127.0.0.1:8001 &
}

# Main deployment process
main() {
    update_code
    # install_dependencies
    run_migrations
    # restart_server
    run_collectstatic
    stop_program_on_port
    echo "Deployment successful!"
}

main
