# ===============================
#  CS3100 Encryption Project (Full Stack)
#  Author: Vip Monty (Group 2)
#  Purpose: Run FastAPI backend + static frontend
# ===============================

FROM python:3.11-slim AS app

# Set working directory
WORKDIR /app

# ---- Install dependencies ----
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project folders ----
COPY Backend ./Backend
COPY Frontend ./Frontend
COPY algorithm_package ./algorithm_package

# ---- Expose ports ----
EXPOSE 8000
EXPOSE 5500

# ---- Run both servers ----
# Start the frontend (static HTML on port 5500)
# and the backend (FastAPI on port 8000) in parallel
CMD ["sh", "-c", "python -m http.server 5500 --directory Frontend & uvicorn Backend.main:app --host 0.0.0.0 --port 8000"]
