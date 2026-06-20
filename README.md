# Healix Pharma Platform 🏥

**Healix** is a state-of-the-art, full-stack Enterprise Pharmaceutical platform. It serves as a highly authoritative **Interactive Visual Aid (e-Detailing)** tool for doctors to explore clinical product compositions, while featuring an AI-driven RAG chatbot and a robust Admin dashboard.

This project consists of three major architectural pillars:
1. **Python / FastAPI Backend** (with RAG AI capabilities)
2. **React Web Application** (Clinical Dashboard & Admin Portal)
3. **Flutter Mobile Application** (Cross-platform Doctor Visual Aid App)

---

## 🌟 Key Features & Accomplishments

### 1. Enterprise "Glassmorphism" UI/UX Design
We completely overhauled the design language across both Web and Mobile to match top-tier pharmaceutical giants (like Pfizer and Sun Pharma), combining authoritative clinical structure with modern 3D Glassmorphism.
- **Sterile Liquid Environments:** Built custom CSS/Flutter animated gradients that serve as a clean, clinical background.
- **Frosted Glass Showcase Cards:** Transitioned from basic grids to massive, horizontal "Showcase" cards featuring heavy background blurs (`backdrop-filter`), razor-thin borders, and deep drop shadows.
- **3D Breakout Imagery:** Product images physically "pop out" of the frosted glass with custom drop shadows.
- **Native-Feeling Animations:** Built buttery-smooth, staggered load animations and physical press-scale reactions in the Flutter app using `TweenAnimationBuilder` and `AnimatedScale`.

### 2. AI-Powered Clinical RAG Chatbot (Backend)
- Implemented a complete Retrieval-Augmented Generation (RAG) pipeline using **Google Gemini (`embedding-001` & `gemini-1.5-pro`)**.
- **Vector DB Construction:** The backend actively scrapes all product clinical profiles, ingredients, and dosages to generate and store high-dimensional embeddings in PostgreSQL.
- **Thread-Safe Background Workers:** Solved complex SQLAlchemy `DetachedInstanceError` crashes by restructuring the background ingestion tasks to use isolated, thread-safe `SessionLocal` contexts.

### 3. Bulletproof Admin Dashboard (Frontend)
- Engineered a robust React-based administrative dashboard for managing the clinical drug catalog.
- Debugged and resolved complex silent failure states in multipart-form data uploads (fixing hidden file input constraints).
- Implemented stable eager-loading DB architectures to ensure cascading category deletions happen safely without database locking.

---

## 🛠 Tech Stack

### Frontend (Web)
- **Framework:** React + Vite
- **Styling:** Tailwind CSS (with highly customized Glassmorphism filters)
- **Animation:** Framer Motion (Staggered spring physics & layout animations)
- **Routing:** React Router DOM

### Mobile App (iOS / Android)
- **Framework:** Flutter (Dart)
- **Architecture:** Responsive Grid/List hybrids using `MediaQuery` constraints for seamless Phone-to-Tablet transitions.
- **Animations:** Custom Flutter `PageRouteBuilder` Hero transitions, `TweenAnimationBuilder` staggered lists.

### Backend & AI
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **AI Integration:** Google Gemini SDK for LLM responses and Vector Embeddings
- **Task Management:** FastAPI `BackgroundTasks` for asynchronous vector indexing.

---

## 🚀 How to Run Locally

### 1. Backend API
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. React Web Interface
```bash
cd frontend
npm install
npm run dev
```

---

*Designed and Developed as a showcase of Enterprise Full-Stack Engineering, AI Integration, and High-End UX/UI Development.*
