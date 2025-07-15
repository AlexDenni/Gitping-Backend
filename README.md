# 🚀 Git Ping — GitHub Action Tracker

Git Ping is a real-time tracker for GitHub events like `PUSH`, `PULL_REQUEST`, and `MERGE`. It uses **Flask** for backend, **MongoDB Atlas** for storage, and a **React** frontend to display updates every 15 seconds.

---

## 🏗️ Architecture
```
GitHub Repo → Webhook → Flask API → MongoDB Atlas → React Frontend
```

---

## 🔧 Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: React + Vite + TailwindCSS
- **Database**: MongoDB Atlas (Cloud NoSQL)
- **Hosting Options**: Heroku, Railway, DigitalOcean

---

## 🌟 Features
- Real-time GitHub event tracking
- Responsive and animated UI
- Auto-polling every 15 seconds
- Color-coded event types
- REST API with sample/testing routes
- Webhook + MongoDB schema integration

---

## 📁 Project Structure
```
git-ping/
├── backend/     # Flask API server
│   └── src/     # Main app, DB, routes, models
├── frontend/    # React UI
└── README.md
```

---

## ⚙️ Quick Setup

### 1. Clone & Backend Setup
```bash
git clone https://github.com/your-repo/git-ping
cd git-ping/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Edit MongoDB URI & PORT
python src/main.py
```

### 2. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev --host  # Dev mode
```

---

## 🪝 GitHub Webhook

1. Go to your GitHub repo → Settings → Webhooks → Add webhook  
2. Payload URL: `http://localhost:5000/api/webhook` (or your live URL)  
3. Content type: `application/json`  
4. Select: ✅ Pushes ✅ Pull Requests  

---

## 🧪 Test Routes

- `POST /api/events/sample` → Create dummy events  
- `GET /api/events` → Fetch events  
- `GET /api/health` → Check backend  

Use [ngrok](https://ngrok.com/) for webhook testing on localhost:
```bash
ngrok http 5000
```

---

## 🧠 MongoDB Schema
```js
{
  request_id: String,
  author: String,
  action: "PUSH" | "PULL_REQUEST" | "MERGE",
  from_branch: String,
  to_branch: String,
  timestamp: String
}
```

---

## 🚀 Deployment

- **Frontend Build**: `npm run build`
- Copy `frontend/dist/` → `backend/src/static/`
- Start backend: `python src/main.py`

---

## 🔒 Tips
- Use `.env` for secrets, never push it
- Enable CORS properly
- Use HTTPS and webhook secret for security
- Restrict MongoDB IP access

---

## 🐞 Common Fixes
- **MongoDB Fail**: Check URI & IP whitelist  
- **No Events**: Check webhook delivery logs  
- **Frontend Blank**: Make sure build is copied  
- **CORS Issues**: Fix in Flask settings  

---
