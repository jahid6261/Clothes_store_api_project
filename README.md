# 🛒 Clothing Store API

A production-style **e-commerce backend API** for a clothing store built with **FastAPI, PostgreSQL, Docker, Celery, RabbitMQ, Cloudinary, SSLCommerz, and AI/RAG integration**.

The API provides authentication, product and variant management, cart, checkout, orders, payments, reviews, admin dashboard, email automation, and an AI-powered shopping assistant.

---

## 🚀 Key Features

### 🔐 Authentication & Security

* User registration and JWT authentication
* Email verification and account activation
* User profile management
* Forgot password with OTP
* Password reset using OTP with expiry
* Secure password hashing
* Role-based access control

### 👕 Product Management

* Category CRUD
* Product CRUD
* Product variants
* Size, color and stock management
* Cloudinary image upload
* Product filtering and pagination
* Bulk product creation and deletion

### 🛒 Cart & Orders

* Add/update/remove cart items
* Cart checkout summary
* Order creation and management
* User order history
* Order cancellation
* Admin order status management
* Automatic stock management

### 💳 Payment

Integrated with **SSLCommerz Payment Gateway**.

Payment flow:

```text
Create Order
     ↓
Create Payment Session
     ↓
SSLCommerz
     ↓
Success / Fail / Cancel
     ↓
Update Order
     ↓
Send Confirmation Email
```

### ⭐ Review System

* Product ratings and comments
* Review validation
* Reviews restricted to completed purchases

### 👨‍💼 Admin Dashboard

* User statistics
* Product statistics
* Order statistics
* Revenue calculation
* Order management
* Order status updates

---

# 📧 Email & Background Tasks

Email automation is implemented using **Celery + RabbitMQ**.

Used for:

* Registration verification emails
* Password reset OTP emails
* Order confirmation emails
* Background email processing

```text
FastAPI
   ↓
Celery
   ↓
RabbitMQ
   ↓
Email Service
```

---

# 🤖 AI Shopping Assistant

The project includes an AI shopping assistant powered by:

* **Ollama**
* **Phi-3**
* **Sentence Transformers**
* **PostgreSQL + pgvector**
* **RAG**
* **Vector Embeddings**

The assistant uses product information stored in the database to answer shopping-related questions.

## RAG Pipeline

```text
User Query
    ↓
Generate Embedding
    ↓
pgvector Similarity Search
    ↓
Retrieve Relevant Product Chunks
    ↓
Product Context
    ↓
Ollama Phi-3
    ↓
AI Response
```

### Example

```text
User:

Show me a cotton t-shirt under 1000 BDT.

AI:

I found cotton t-shirts matching your price range...
```

### Embedding

Product information is converted into vector embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embeddings are stored in PostgreSQL using **pgvector** for semantic similarity search.

This allows the AI assistant to understand product-related queries beyond simple keyword matching.

---

# 🐳 Docker

The application is containerized using **Docker Compose**.

The FastAPI application image is available on Docker Hub:

```text
jahidalam/clothstore-api:latest
```

Main services:

* FastAPI
* PostgreSQL
* pgvector
* PgAdmin
* RabbitMQ
* Celery Worker

The application uses the pre-built Docker Hub image, so clients do **not** need to build the FastAPI image locally.

### Start the application

```bash
docker compose pull
docker compose up -d
```

### Check services

```bash
docker compose ps
```

### View logs

```bash
docker compose logs -f web
```

### Stop services

```bash
docker compose down
```

---

# 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy Async
* Alembic

### Database

* PostgreSQL
* pgvector

### Authentication

* JWT
* Password Hashing
* OTP Password Reset

### Storage

* Cloudinary

### Background Processing

* Celery
* RabbitMQ

### Payment

* SSLCommerz

### AI / RAG

* Ollama
* Phi-3
* Sentence Transformers
* Vector Embeddings
* pgvector
* RAG

### DevOps

* Docker
* Docker Compose
* Git
* GitHub
* Docker Hub

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/jahid6261/Clothes_store_api_project.git

cd Clothes_store_api_project
```

## 2. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

SECRET_KEY=
ALGORITHM=HS256

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=
EMAIL_PASSWORD=
EMAIL_FROM=

CELERY_BROKER_URL=

BASE_URL=http://localhost:8001

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

SSLCOMMERZ_STORE_ID=
SSLCOMMERZ_STORE_PASSWORD=
SSLCOMMERZ_PAYMENT_URL=
SSLCOMMERZ_VALIDATION_URL=
SSLCOMMERZ_SUCCESS_URL=
SSLCOMMERZ_FAIL_URL=
SSLCOMMERZ_CANCEL_URL=

ADMIN_EMAIL=
ADMIN_PASSWORD=

RABBITMQ_DEFAULT_USER=
RABBITMQ_DEFAULT_PASS=
```

> **Important:** Never commit the real `.env` file to GitHub. Use `.env.example` for sharing the required environment variables.

## 3. Pull Docker Images

```bash
docker compose pull
```

## 4. Start the Application

```bash
docker compose up -d
```

## 5. Run Database Migrations

```bash
docker compose exec web alembic upgrade head
```

## 6. Check Running Containers

```bash
docker compose ps
```

---

# 🤖 Ollama Setup

The AI assistant uses **Ollama + Phi-3**.

Install Ollama on the host machine and pull the model:

```bash
ollama pull phi3
```

Start Ollama:

```bash
ollama serve
```

> **Note:** The FastAPI container must be able to reach the Ollama service. When running Ollama directly on the host machine, configure the application's Ollama URL according to the Docker host networking setup.

### AI Endpoint

```http
POST /ai/chat
```

Example request:

```json
{
  "prompt": "Show me available cotton t-shirts."
}
```

---

# 📚 API Documentation

After starting the application:

### Swagger UI

```text
http://localhost:8001/docs
```

### ReDoc

```text
http://localhost:8001/redoc
```

---

# 🔄 Application Architecture

```text
                    Client
                      │
                      ▼
              FastAPI Application
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   PostgreSQL     RabbitMQ      Cloudinary
   + pgvector         │
                      ▼
                 Celery Worker
                      │
                      ▼
                 Email Service

                      │
                      ▼
                 AI Assistant
                      │
              ┌───────┴────────┐
              ▼                ▼
        pgvector RAG         Ollama
              │                │
              └───────┬────────┘
                      ▼
                  Phi-3
```

---

# 📦 Docker Services

| Service             | Purpose             |  Port |
| ------------------- | ------------------- | ----: |
| FastAPI             | Backend API         |  8001 |
| PostgreSQL          | Database + pgvector |  5433 |
| PgAdmin             | Database management |  5051 |
| RabbitMQ            | Message broker      |  5673 |
| RabbitMQ Management | RabbitMQ dashboard  | 15673 |

---

# 🔑 Important Environment Variables

The application requires external services for some features:

* PostgreSQL
* RabbitMQ
* Cloudinary
* SMTP/Email
* SSLCommerz
* Ollama

Without the corresponding credentials/configuration, those specific features will not work.

---

# 👨‍💻 Author

**Jahid Alam**

Python Backend Developer

**Tech:** FastAPI • PostgreSQL • Docker • Celery • RabbitMQ • AI/RAG

GitHub:

https://github.com/jahid6261
