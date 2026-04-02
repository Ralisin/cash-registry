# 📊 Telegram Finance App – Full Stack Project (Vue3 + MongoDB + Free Hosting)

## 🎯 Goal

Build a complete personal finance management system integrated with Telegram.

The system must include:

* Telegram bot
* Backend API
* Web UI (Telegram Web App)

Users must be able to track expenses, manage balances (cash and card), and visualize financial data.

---

## 🧱 Tech Stack (MANDATORY)

### Backend

* Python
* FastAPI

### Database

* MongoDB (use MongoDB Atlas free tier)
* Use an ODM (Motor or Beanie preferred)

### Frontend

* Vue 3 (Composition API)
* Mobile-first design
* Runs as Telegram Web App

### Bot

* Telegram Bot API
* python-telegram-bot

---

## ☁️ Hosting (FREE ONLY)

You MUST structure the project to be deployed like this:

* Backend → Render (free tier)
* Frontend → Vercel (free tier)
* Database → MongoDB Atlas (free tier)

Take into account:

* Render sleeps after inactivity
* Use environment variables
* Use HTTPS endpoints

---

## 🧠 Architecture

```
Frontend (Vercel - Vue3)
↓
Backend API (Render - FastAPI)
↓
MongoDB Atlas

Telegram Bot → communicates with Backend
```

---

## 👤 User Model

Each user is identified via Telegram.

Fields:

* telegram_id
* name
* created_at

---

## 💰 Financial System

### Accounts

Each user has:

* cash balance
* card balance

---

### Transactions

Each transaction must include:

* id
* user_id
* amount
* type (expense, income, transfer)
* source_account (cash/card)
* destination_account (for transfers)
* category
* note
* date (custom date allowed)
* created_at

---

## 🔁 Core Features

### 1. Initial Setup

* Set initial balances:

  * cash
  * card

---

### 2. Add Expense

* amount
* category
* account
* note (optional)
* custom date

---

### 3. Add Income

* same as expense but adds money

---

### 4. Transfer

* card → cash
* cash → card

---

### 5. History

* list transactions
* filters:

  * date
  * category
  * type

---

### 6. Dashboard

* total balance
* cash
* card
* recent transactions

---

### 7. Analytics

* monthly spending
* category breakdown
* charts

---

## 🌐 API Requirements

Create REST endpoints:

* POST /users
* GET /users/{telegram_id}
* POST /transactions
* GET /transactions
* GET /transactions/{id}
* POST /transfer
* GET /balance

---

## 🤖 Telegram Bot Behavior

Commands:
* /start → register user
* /app → open web app

Bot must include button:

* "Open Finance App"

This button must open the Telegram Web App (hosted on Vercel)

---

## 🔐 Authentication

Use Telegram Web App initData.

Backend must:

* validate initData
* extract telegram user info

---

## 🎨 Frontend (Vue 3)

### Pages:

* Dashboard
* Add Transaction
* History
* Analytics

### Requirements:

* clean UI
* mobile optimized
* simple UX
* API integration

---

## ⚙️ Deployment Instructions (IMPORTANT)

You MUST include:

### Backend (Render)

* requirements.txt
* start command:
  ```
  uvicorn main:app --host 0.0.0.0 --port 10000
  ```

---

### Frontend (Vercel)

* build command:
  ```
  npm run build
  ```
* output folder:
  ```
  dist
  ```

---

### MongoDB

* connection via environment variable

---

## 🚀 Output Requirements

Generate:

1. Backend code (FastAPI + MongoDB)
2. Models (ODM)
3. API routes
4. Telegram bot code
5. Vue 3 frontend
6. Instructions to run locally
7. Deployment guide (Render + Vercel + MongoDB Atlas)

---

## ⚠️ Constraints

* Clean, modular architecture
* Use environment variables
* Production-ready structure
* Comment the code
* Avoid unnecessary complexity

---

## 🧠 Instructions for Claude

Generate the project STEP-BY-STEP:

1. Backend structure
2. Database models
3. API routes
4. Telegram bot
5. Frontend (Vue 3)
6. Deployment

DO NOT generate everything at once.

Wait for confirmation before moving to next step.

---

## 💬 Notes

Per qualsiasi dubbio chiedi e ti do chiarimenti/linee guida sul progetto
