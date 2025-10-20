# Dual Defense

Dual Defense is a Vanilla JS Front end, FastAPI Backend. Custom Algorithm to demonstrate Sufficient Encryption & Input Validation.


## Overview
Web Page input takes message -> Validates Input -> Sends to Backend API -> Encryption Applied to message -> Stores in SQLalchemy Database.



## Setup

1. Clone Repo

```bash
git clone https://github.com/PhysicistsOfDoom/CS-3100-CryptoAlgorithm.git
cd CS-3100-CryptoAlgorithm
```
2. Set up Virtual Environment
```
python -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate.bat  # (Windows)
```

3. Install Dependencies (Optional if you choose to run with Docker)

```bash
pip install -r requirements.txt
```

4. Run the Project. There are **3** options!
### Option 1: Scripts/
From the repo root /
```bash
./Scripts/run.sh
```
Windows PowerShell:
```bash
.\Scripts\run.bat 
```

### Option 2: Docker Compose

```bash
docker-compose up --build
```
### Option 3: Manually

```bash
# Start Backend
cd Backend/
uvicorn Backend.main:app --reload

# Start Frontend
cd ../Frontend
python -m http.server 3000
```
## Usage
When both servers are running: The pages by default are accessible via:
```
Backend API: http://localhost:8000
Frontend: http://localhost:3000
```
## Tech Stack
- FastAPI
- SQLAlchemy
- Python 3.11
- HTML, CSS, JavaScript

## Contributing

This is a UVU Team demonstrating knowledge of encryption across networks. Both across the wire, through APIs and Storage.


## License

[MIT](https://choosealicense.com/licenses/mit/)