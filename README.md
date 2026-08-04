# 🛒 Clothing Store API

A complete **e-commerce backend API** for a clothing store built with **FastAPI, PostgreSQL, Docker, Celery, RabbitMQ, Cloudinary, SSLCommerz Payment Gateway, and AI integration using Ollama Phi-3**.

The system provides complete online shopping functionality including authentication, product management, cart, checkout, order processing, payment, reviews, admin dashboard, email verification, background task processing, and an AI shopping assistant.

---

# 🚀 Features

## 🔐 Authentication System

* User registration
* JWT authentication
* User login
* User profile management
* Email verification after registration
* Account activation using verification token

---

# 👕 Product Management

* Category CRUD
* Product CRUD
* Product variants management
* Size and color management
* Stock management
* Product image upload
* Product filtering and pagination
* Bulk product creation
* Bulk product deletion

### Cloudinary Integration

Cloudinary is used for product image management.

Features:

* Upload product variant images
* Store image URLs securely
* Delete product images
* Cloud-based image storage

---

# 🛒 Cart & Checkout System

Features:

* Add product to cart
* Update cart item quantity
* Remove cart items
* Clear cart
* Checkout summary generation

---

# 📦 Order Management

Features:

* Create orders
* View user orders
* Order details
* Cancel orders
* Admin order management
* Update order status

---

# 💳 Payment Integration

Integrated with **SSLCommerz Payment Gateway**.

Payment flow:

1. User creates order
2. Payment session is generated
3. Customer completes payment
4. Payment callback is received
5. Order status is updated
6. Confirmation email is sent

Features:

* Create payment session
* Payment success handling
* Payment failure handling
* Payment cancellation handling

---

# ⭐ Review System

Features:

* Product rating system
* Product Comment system
* Review validation
* Only completed orders can submit reviews

---

# 👨‍💼 Admin Dashboard

Features:

* Admin authentication
* Dashboard statistics
* Total users count
* Total products count
* Total orders count
* Revenue calculation
* Order management
* Update order status

---

# 📧 Email Verification & Notification System

Implemented email automation system.

Email features:

* Registration verification email
* Account activation link
* Order confirmation email after successful payment

Email workflow:

```
User Registration
        |
        |
Generate Activation Token
        |
        |
Celery Task
        |
        |
RabbitMQ Queue
        |
        |
Send Email
```

---

# ⚡ Background Task Processing

Implemented asynchronous task processing using:

* Celery
* RabbitMQ

Used for:

* Sending verification emails
* Sending order confirmation emails
* Running background jobs without blocking API requests

Architecture:

```
FastAPI
   |
   |
Celery Worker
   |
   |
RabbitMQ
   |
   |
Email Service
```

---

# 🤖 AI Shopping Assistant

Integrated AI chatbot using:

* Ollama
* Phi-3 Language Model
* Database-backed responses

The AI assistant answers user questions using product data stored in PostgreSQL.

Example:

```
User:
What is the price of Classic Cotton T-Shirt?

AI:
According to the database, Classic Cotton T-Shirt price is 850.00 BDT.
```

Future AI improvements:

* RAG pipeline
* ChromaDB integration
* FAISS vector search
* Whisper voice assistant
* AI recommendation system

---

# 🐳 Docker Implementation

The entire application is containerized using Docker.

Docker services:

* FastAPI Backend
* PostgreSQL Database
* PgAdmin
* RabbitMQ
* Celery Worker

Benefits:

* Easy setup
* Environment consistency
* Service isolation
* Production-ready deployment

Run project:

```bash
docker compose up -d
```

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy Async
* Alembic

## Database

* PostgreSQL

## Authentication

* JWT Authentication
* Password Hashing

## Storage

* Cloudinary

## Background Processing

* Celery
* RabbitMQ

## Payment

* SSLCommerz

## AI

* Ollama
* Phi-3 Model

## DevOps

* Docker
* Docker Compose
* Git & GitHub

---

# 📂 Project Structure
```text
Clothes_store_api_project/
│
├── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
│
├── src/
│   │
│   ├── users/
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── products/
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── orders/
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── payments/
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── sslcommerz.py
│   │
│   ├── admin/
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── ai/
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   ├── prompt.py
│   │   └── service.py
│   │
│   ├── cart/
│   │
│   ├── core/
│   │   ├── celery.py
│   │   ├── email.py
│   │   └── task.py
│   │
│   ├── depends/
│   │
│   ├── seed/
│   │
│   └── utils/
│
├── alembic/
│   ├── env.py
│   └── versions/
│
└── README.md
```



# ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/jahid6261/Clothes_store_api_project

cd Clothes_store_api_project
```

Create `.env` file:

```
# Database
DATABASE_URL=

# Security
SECRET_KEY=
ALGORITHM=HS256


# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_FROM=


# Celery / RabbitMQ
CELERY_BROKER_URL=

# Base URL
BASE_URL=http://localhost:8001


# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=


# SSLCommerz Payment Gateway
SSLCOMMERZ_STORE_ID=
SSLCOMMERZ_STORE_PASSWORD=

SSLCOMMERZ_PAYMENT_URL=
SSLCOMMERZ_VALIDATION_URL=

SSLCOMMERZ_SUCCESS_URL=
SSLCOMMERZ_FAIL_URL=
SSLCOMMERZ_CANCEL_URL=


# Admin Account
ADMIN_EMAIL=
ADMIN_PASSWORD=
```

---

# 🐳 Run With Docker

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

---

# 🗄️ Database Migration

Run migration:

```bash
docker compose exec web alembic upgrade head
```

---

# 🤖 Ollama Setup

Install Phi-3 model:

```bash
ollama pull phi3
```

Run Ollama:

```bash
ollama serve
```

AI endpoint:

```
POST /ai/chat
```

Request:

```json
{
  "prompt": "What products are available?"
}
```

---

# 📚 API Documentation

Swagger UI:

```
http://localhost:8001/docs
```

---

# 🔗 API Modules

## Authentication

```
POST   /users/register
POST   /users/login
GET    /users/profile
GET    /users/activate/{token}
```

## Products

```
GET    /products/
POST   /products/
GET    /products/{product_id}
POST   /products/categories
POST   /productsvariants
```

## Cart

```
POST   /cart/items
GET    /cart
POST   /cart/checkout
```

## Orders

```
POST   /orders/create
GET    /orders
GET    /orders/{order_id}
```

## Payment

```
POST   /payment/create
POST   /payment/success
POST   /payment/cancel
POST   /payment/fail
```

## Admin

```
GET    /admin/dashboard
GET    /admin/orders
PATCH  /admin/orders/{order_id}/status
```

## AI

```
POST   /ai/chat
```

---

# 🌱 Future Improvements

* RAG based product search
* Vector database integration
* ChromaDB
* FAISS
* Whisper speech recognition
* AI product recommendation
* Chat history memory

---

# 👨‍💻 Author

**Jahid Alam**

Backend Developer

Skills:

* FastAPI
* PostgreSQL
* Docker
* AI Integration

GitHub:

https://github.com/jahid6261
