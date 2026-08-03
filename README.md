# 🚀 SkillOrbit — Peer-to-Peer Skill Swapping Platform

**SkillOrbit** is a modern, full-stack peer-to-peer skill sharing platform built with Django. It connects learners and mentors through **1-on-1 scheduled pair learning sessions**, **community video courses**, and **real-time peer messaging**.

---

## ✨ Key Features

- 📅 **1-on-1 Peer Sessions**: Schedule 1-on-1 skill swap sessions with peers using a custom cross-browser Date & Time picker, interactive status badges (`Pending`, `Accepted`, `Completed`), and instant Jitsi Video meeting rooms.
- 📺 **Community Video Courses**: Browse and publish video tutorials with YouTube thumbnail preview cards and embedded playback.
- 💬 **Real-Time Peer Chat**: Instant 1-on-1 messaging powered by WebSockets and Django Channels.
- 🌐 **Community Forum & Requests**: Post skill request topics, comment, and connect with peers.
- 🎨 **Material Design 3 Theme**: Responsive, dark-mode design system optimized for desktop and mobile browsers.

---

## 🔄 Platform Workflow

```mermaid
graph TD
    A[User Sign In / Sign Up] --> B[Explore Peers & Skills]
    
    B -->|Option 1: 1-on-1 Live Swap| C[Schedule Peer Session]
    C --> C1[Pick Future Date & Time]
    C1 --> C2[Peer Accepts Request]
    C2 --> C3[Join 1-on-1 Jitsi Video Meeting]
    C3 --> C4[Mark Session Completed]
    
    B -->|Option 2: Video Learning| D[Community Video Courses]
    D --> D1[Publish YouTube Tutorial]
    D1 --> D2[Stream & Learn Asynchronously]
    
    B -->|Option 3: Real-Time Chat| E[Live 1-on-1 Chat]
    E --> E1[WebSocket Direct Messaging]
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, Django 6.0, ASGI / Daphne
- **Database**: PostgreSQL / SQLite3
- **Real-Time**: Django Channels & Redis / InMemory Channel Layer
- **Video Meetings**: Jitsi Meet Integration
- **Frontend**: HTML5, Vanilla CSS3 (Material Design 3 Tokens), JavaScript (ES6)

---

## 🚀 Quick Setup & Installation

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/saraths3/SkillOrbit.git
cd SkillOrbit

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Migration
```bash
python SkillOrbit/manage.py migrate
```

### 4. Run Development Server
```bash
python SkillOrbit/manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser!

---

## 📄 License

This project is licensed under the MIT License.
