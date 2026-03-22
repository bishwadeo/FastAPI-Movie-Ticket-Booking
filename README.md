 🎬 Movie Ticket Booking API

## 📌 Project Overview

This project is a FastAPI-based backend system for managing a Movie Ticket Booking platform.
It allows users to browse movies, book tickets, hold seats, confirm bookings, and explore advanced features like search, sorting, and pagination.

This project is developed as part of the **FastAPI Internship Final Assignment** and implements all concepts from Day 1 to Day 6.

---

## 🚀 Features

### ✅ Core Features

* View all movies
* Get movie details by ID
* Movie summary (pricing, seats, genres)
* Book tickets with validation
* Update and delete movies

### ✅ CRUD Operations

* Create movie
* Read movie data
* Update movie price and seats
* Delete movie with validation

### ✅ Multi-Step Workflow

* Seat Hold → Confirm Booking → Release Hold
* Real-time seat availability updates

### ✅ Advanced APIs

* 🔍 Search movies by keyword
* 🎯 Filter by genre, language, price, seats
* 🔄 Sort movies (price, duration, seats)
* 📄 Pagination support
* 🔗 Combined browsing endpoint

---

## 🧠 Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic

---

## 📂 Project Structure

```
project/
│── main.py
│── requirements.txt
│── README.md
│── screenshots/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 2️⃣ Activate Environment

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install fastapi uvicorn
```

### 4️⃣ Run Server

```bash
uvicorn main:app --reload
```

### 5️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### 🏠 Basic Routes

* GET `/` → Welcome message
* GET `/movies` → Get all movies
* GET `/movies/{movie_id}` → Get movie by ID
* GET `/movies/summary` → Summary of movies

---

### 🎟️ Booking System

* POST `/bookings` → Create booking
* GET `/bookings` → View all bookings
* GET `/bookings/search` → Search bookings
* GET `/bookings/sort` → Sort bookings
* GET `/bookings/page` → Pagination

---

### 🎬 Movie Management

* POST `/movies` → Add new movie
* PUT `/movies/{movie_id}` → Update movie
* DELETE `/movies/{movie_id}` → Delete movie

---

### ⏳ Seat Hold Workflow

* POST `/seat-hold` → Hold seats
* POST `/seat-confirm/{hold_id}` → Confirm booking
* DELETE `/seat-release/{hold_id}` → Release seats

---

### 🔍 Advanced Features

* GET `/movies/search` → Keyword search
* GET `/movies/filter` → Filter movies
* GET `/movies/sort` → Sort movies
* GET `/movies/page` → Pagination
* GET `/movies/browse` → Combined filtering + sorting + pagination

---

