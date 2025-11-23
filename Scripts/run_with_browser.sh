#!/bin/bash

# CS-3100 CryptoAlgorithm - Enhanced Run Script
# This script starts the backend, frontend, and opens the browser

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
FRONTEND_URL="http://localhost:$FRONTEND_PORT"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to open URL in browser (cross-platform)
open_browser() {
    local url=$1
    print_status "Opening $url in browser..."

    # Detect OS and use appropriate command
    case "$(uname -s)" in
        Darwin*)    # macOS
            open "$url"
            ;;
        Linux*)     # Linux
            xdg-open "$url" 2>/dev/null || sensible-browser "$url" 2>/dev/null
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)  # Windows
            start "$url"
            ;;
        *)
            print_warning "Could not detect OS. Please manually open: $url"
            ;;
    esac
}

# Function to cleanup background processes
cleanup() {
    print_status "Shutting down services..."

    # Kill background jobs
    if [[ ! -z $BACKEND_PID ]]; then
        kill $BACKEND_PID 2>/dev/null
        print_status "Backend stopped"
    fi

    if [[ ! -z $FRONTEND_PID ]]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend stopped"
    fi

    exit 0
}

# Set up signal handlers for cleanup
trap cleanup SIGINT SIGTERM

# Navigate to project root
cd "$(dirname "$0")"
cd ..

print_status "Starting CS-3100 CryptoAlgorithm Application..."

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    print_status "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    print_status "Activating virtual environment..."
    source .venv/bin/activate
else
    print_warning "No virtual environment found. Using system Python."
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    print_error "Required dependencies not found. Installing from requirements.txt..."
    pip3 install -r requirements.txt
fi

# Check if ports are available
if check_port $BACKEND_PORT; then
    print_error "Port $BACKEND_PORT is already in use. Please free the port or change BACKEND_PORT in this script."
    exit 1
fi

if check_port $FRONTEND_PORT; then
    print_error "Port $FRONTEND_PORT is already in use. Please free the port or change FRONTEND_PORT in this script."
    exit 1
fi

# Start Backend
print_status "Starting backend on port $BACKEND_PORT..."
uvicorn Backend.main:app --reload --port $BACKEND_PORT &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Failed to start backend"
    exit 1
fi

print_status "Backend started successfully (PID: $BACKEND_PID)"

# Start Frontend
print_status "Starting frontend on port $FRONTEND_PORT..."
cd Frontend
python3 -m http.server $FRONTEND_PORT &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 2

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Failed to start frontend"
    cleanup
    exit 1
fi

print_status "Frontend started successfully (PID: $FRONTEND_PID)"

# Wait for services to be fully ready
print_status "Waiting for services to be ready..."
sleep 3

# Open browser
open_browser $FRONTEND_URL

# Display running information
echo
print_status "=== Application Started Successfully ==="
echo -e "  Frontend: ${GREEN}$FRONTEND_URL${NC}"
echo -e "  Backend:  ${GREEN}http://localhost:$BACKEND_PORT${NC}"
echo -e "  API Docs: ${GREEN}http://localhost:$BACKEND_PORT/docs${NC}"
echo
print_status "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait