# 🔐 CS3100 Encryption Project
**Author:** Abdullah Kareem, Corbin Beus, Joashua Slaugh, Tanner Bingham and Vip Monty (Group 2)  
**Course:** CS 3100 — Data Privacy and Security  

This project demonstrates a **full-stack encryption web application** built with **FastAPI (backend)** and a **HTML/CSS/JavaScript (frontend)** interface.  
Users can enter plain text messages, encrypt them, store them securely in a SQLite database, and retrieve the decrypted version later.

---

## 🌐 Features

✅ **Frontend (User Interface)**
- Simple and intuitive HTML/CSS form design.  
- Allows users to:
  - Submit a message for encryption.
  - Retrieve a decrypted message by name.
- Displays clear visual feedback for encrypted and decrypted data.

✅ **Backend (FastAPI)**
- Uses **Fernet symmetric encryption** for secure message handling.
- Stores each encrypted message and key in **SQLite**.
- Provides REST endpoints for:
  - `POST /message` — Encrypt and store a message.
  - `GET /message/{name}` — Retrieve and decrypt a message.
- Cross-Origin Resource Sharing (CORS) enabled for frontend communication.

✅ **Database**
- Simple SQLite database (`app.db`) managed through SQLAlchemy.
- Automatically created at startup.

---

## 🗂️ Project Structure
<pre> ```
CS-3100-CryptoAlgorithm/
│
├── Backend/
│ ├── main.py # FastAPI entry point
│ ├── db.py # Database connection setup
│ ├── models.py # SQLAlchemy Message model
│ ├── algorithm_package/
│ │ └── string_encryption.py # Encryption & decryption logic
│ └── app.db # SQLite database (auto-created)
│
├── Frontend/
│ ├── index.html # User interface
│ ├── index.js # Handles frontend API calls
│ ├── styles.css # Layout and styling
│
├── requirements.txt # Python dependencies
├── docker-compose.yml # Optional Docker setup
├── setup.py # Project setup script
└── README.md # You are here

``` </pre>

---

## 🚀 Getting Started

 

```bash
1️⃣ Clone the Repository
git clone https://github.com/PhysicistsOfDoom/CS-3100-CryptoAlgorithm.git
cd CS-3100-CryptoAlgorithm

2️⃣ Create and Activate a Virtual Environment
python -m venv venv
source venv/Scripts/activate    # On Windows
# OR
source venv/bin/activate        # On Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Backend (FastAPI) from CS-3100-CryptoAlgorithm/
uvicorn Backend.main:app --reload
The backend will start at
👉 http://127.0.0.1:8000

You can test API routes directly here:
👉 http://127.0.0.1:8000/docs

5️⃣ Run the Frontend
Open another terminal:
cd Frontend
python -m http.server 5500
Then visit:
👉 http://127.0.0.1:5500 or localhost:5500

6️⃣ Access backend database
ctrl + c if backend server is running
from CS-3100-CryptoAlgorithm/
python view_db.py


🧠 How It Works
User enters a message in the frontend form.
The message is sent via a POST request to the FastAPI backend.

The backend:
Generates a unique encryption key.
Encrypts the message using the key.
Stores both in the SQLite database.
When the user requests the same name, the backend decrypts the message and returns it.

📡 API Endpoints
Method	Endpoint	Description
GET	/	Health check / Welcome message
POST	/message	Encrypts and stores a new message
GET	/message/{name}	Retrieves and decrypts a stored message

Example JSON Payload:
POST /message
json

{
  "name": "vip",
  "message": "hello team!"
}
Response:
json

{
  "id": 1,
  "name": "vip",
  "encrypted_message": "gAAAAABlW...",
  "key": "f-KxK2fHS..."
}
🛠️ Technologies Used
Python 3.11+
FastAPI
SQLAlchemy
Cryptography (Fernet)
HTML / CSS / JavaScript
SQLite

📘 Example Workflow
Start backend → uvicorn Backend.main:app --reload (from root directory, which contains both backend and frontend directory)

Start frontend → python -m http.server 5500 (from frontend directory)

Open browser → http://127.0.0.1:5500 or localhost:5500

Enter:

Name: vip
Message: hello team!
Click Encrypt & Send
→ You’ll see the encrypted text and key displayed.

Enter the same name under Get Message
→ The decrypted message “hello team!” appears.

🧹 .gitignore Recommendation
To avoid clutter in version control, include this in your .gitignore:


venv/
Scripts/
__pycache__/
*.db
.env

==Dockerfile will need Docker Desktop Installer.exe installed to initial APP using Dockerfile Method==
🐳 Running the Project with Docker

This project includes a preconfigured Dockerfile so you can run the entire FastAPI backend and static frontend inside one container.

✅ 1️⃣ Build the Docker image

From your project root (CS-3100-CryptoAlgorithm/):

docker build -t cs3100-encryption-app .


Docker will:

Download a lightweight Python 3.11 image

Install dependencies (including Git)

Copy your project files

Configure both the FastAPI backend (port 8000) and the static frontend (port 5500)

✅ 2️⃣ Run the container
docker run -d -p 8000:8000 -p 5500:5500 cs3100-encryption-app

Service	URL
🌐 Frontend	http://127.0.0.1:5500

⚙️ Backend API	http://127.0.0.1:8000

📘 Swagger Docs	http://127.0.0.1:8000/docs
✅ 3️⃣ Stop or remove the container

List containers:

docker ps


Stop a running one:

docker stop <container_id>


Remove old containers (optional):

docker rm <container_id>

⚙️ Troubleshooting
Issue	Solution
port is already allocated	Stop the existing container using port 8000: docker ps → docker stop <id>
Frontend changes not showing	Rebuild the image: docker build --no-cache -t cs3100-encryption-app .
Form not resetting inside Docker	Added <meta http-equiv="Cache-Control"> tags in index.html to prevent browser caching
🧹 Cleanup commands

Remove all stopped containers and dangling images:

docker system prune -af

🧠 Quick Summary

Build once → docker build -t cs3100-encryption-app .

Run anywhere → docker run -d -p 8000:8000 -p 5500:5500 cs3100-encryption-app

Visit → http://127.0.0.1:5500