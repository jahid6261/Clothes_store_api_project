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

## 📧 Email & Background Tasks

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

### RAG Pipeline

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

This allows the AI assistant to understand queries beyond simple keyword matching.

---

# 🐳 Docker

The application is containerized using Docker Compose.

Main services:

* FastAPI
* PostgreSQL
* pgvector
* PgAdmin
* RabbitMQ
* Celery Worker

Run:

```bash
docker compose build
docker compose up -d
```

Check services:

```bash
docker compose ps
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



# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/jahid6261/Clothes_store_api_project.git

cd Clothes_store_api_project
```

Create a `.env` file and configure:

```env
DATABASE_URL=

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
```

Run Docker:

```bash
docker compose up -d
```

Run migrations:

```bash
docker compose exec web alembic upgrade head
```

---

# 🤖 Ollama Setup

Install Ollama and pull the Phi-3 model:

```bash
ollama pull phi3
```

Start Ollama:

```bash
ollama serve
```

AI endpoint:

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

Swagger UI:

```text
http://localhost:8001/docs
```





# 👨‍💻 Author

**Jahid Alam**

Python Backend Developer

**Tech:** FastAPI • PostgreSQL • Docker • Celery • RabbitMQ • AI/RAG

GitHub:
https://github.com/jahid6261
