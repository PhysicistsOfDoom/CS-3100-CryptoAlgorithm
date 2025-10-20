#!/bin/bash

cd "$(dirname "$0")"
cd ..

# Start Backend
echo "Starting backend..."
uvicorn Backend.main:app --reload &

# Start Frontend
echo "Starting frontend..."
cd Frontend
python -m http.server 3000