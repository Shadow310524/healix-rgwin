# Healix Pharmaceutical Platform (RG WIN HEALTHCARE)

A modern, full-stack pharmaceutical platform built for RG WIN HEALTHCARE. It includes a professional public-facing website for customers to explore products, and a secure, authenticated Admin Dashboard to manage inventory, categories, and customer enquiries.

## 🚀 How to Start the Project

This project uses a React frontend and a FastAPI backend with PostgreSQL.

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+)
*   PostgreSQL (Running locally on port 5432)

### 1. Start the Backend (FastAPI)
Open a terminal and navigate to the `backend` folder:
```bash
cd backend

# (Optional) Activate your virtual environment if you have one
# .\venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the backend server
python -m uvicorn main:app --reload
```
*The API will be running at `http://127.0.0.1:8000`.*
*(You can view the interactive API documentation at `http://127.0.0.1:8000/docs`)*

### 2. Start the Frontend (React + Vite)
Open a **new** terminal and navigate to the `frontend` folder:
```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Run the development server
npm run dev
```
*The website will be running at `http://localhost:5173`.*

### Admin Access
You can access the admin panel at `http://localhost:5173/admin/login`.
*   **Email**: `admin@healixtest.com`
*   **Password**: `admin123`

---

## ✅ Features Currently Implemented

### Public Website
*   **Modern UI/UX**: Professional medical aesthetic using Tailwind CSS and Framer Motion animations.
*   **Dynamic Product Catalog**: The Products and Product Details pages fetch live data directly from the PostgreSQL database.
*   **Contact Form**: Fully functional contact form that sends customer enquiries directly to the database with real-time UI toast notifications.

### Backend & API (FastAPI)
*   **PostgreSQL Database**: fully integrated using SQLAlchemy models and Alembic migrations.
*   **JWT Authentication**: Secure, hashed (`bcrypt`), token-based authentication for all admin routes.
*   **RESTful Endpoints**: Complete CRUD operations built for `Products`, `Categories`, and `Enquiries`.

### Admin Dashboard (React)
*   **Secure Access**: Protected routes that require valid JWT tokens. Interceptors automatically attach credentials to outgoing API requests.
*   **Real-time Enquiries Viewer**: Auto-refreshing table (every 30 seconds) with a Modal pop-up to read customer feedback in real-time.
*   **Inventory Management**: Modals to create new Products and Categories on the fly.
*   **Toast Notifications**: Global UI alerts (`react-hot-toast`) for successful actions or errors.

---

## 🚧 Features Yet to Complete (Roadmap)

### 1. Image Uploads (Cloudinary Integration)
*   Currently, product images require a manual URL input.
*   **To Do**: Integrate Cloudinary API in the backend to allow the admin to upload physical image files from their computer directly into the "Add Product" modal.

### 2. AI Chatbot Integration (RAG)
*   **To Do**: Build the backend `/api/v1/chat/` endpoint using the **Google Gemini API** (or chosen LLM). 
*   **To Do**: Implement strict RAG (Retrieval-Augmented Generation) using `system_prompts.py` so the bot only answers using valid RG WIN HEALTHCARE product descriptions.
*   **To Do**: Build the floating chat widget on the frontend website.

### 3. Advanced Admin AI Tools
*   **To Do**: Implement the AI Product Description Generator (auto-write marketing copy for new products).
*   **To Do**: Implement Semantic Smart Search for the products page.
*   **To Do**: Add Enquiry Sentiment Analysis to badge incoming customer messages (e.g., *Urgent*, *Sales*).

### 4. Final Polish & Deployment
*   **To Do**: Comprehensive form validation.
*   **To Do**: Prepare production environment variables.
*   **To Do**: Deploy Frontend (Vercel) and Backend (Render/Heroku).
