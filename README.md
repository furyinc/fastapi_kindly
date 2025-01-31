# ✨ Donation App

A minimalistic donation platform where users can donate for specific events.

## 🔧 Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** MySQL
- **Authentication:** JWT Authorization
- **Containerization:** Docker

## 📅 Features
- Users can donate to various events
- Secure authentication using JWT
- **Coming Soon:** Payment integration with **PayPal/Stripe/Click**

## ⚡ Quick Start

### **1. Clone the Repository**
```sh
git clone https://github.com/furyinc/fastapi_kindly.git
cd donation-app
```

### **2. Set Up Environment Variables**
Create a `.env` file in the root directory:
```sh
MYSQL_ROOT_PASSWORD=yourpassword
MYSQL_DATABASE=donation_db
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
```

### **3. Build & Run with Docker**
```sh
docker-compose up --build
```
This starts the backend and MySQL database.

### **4. Access the API**
- **API Base URL:** `http://localhost:8000`
- **Docs:** `http://localhost:8000/docs`

## 🛠 Managing the App
- **Stop Containers:** `docker-compose down`
- **Stop & Remove Volumes:** `docker-compose down -v`

## 🛠️ Contributing
Feel free to contribute by creating a pull request!

## 📜 License
This project is licensed under the [MIT License](LICENSE.txt).


