# 🌱 AgroGuideAI

An AI-powered smart agriculture platform built with Django and Machine Learning that helps farmers make informed decisions through crop recommendation, plant disease detection, weather insights, and an AI farming assistant.

## 🚀 Features

- 🌾 Crop Recommendation based on weather and soil conditions
- 🍃 Plant Disease Detection using Deep Learning (CNN)
- 🌦️ Real-time Weather Information
- 🤖 AI Farming Assistant (OpenRouter AI)
- 👤 User Authentication (Register/Login)
- 📊 Crop Prediction using Machine Learning
- 📱 Responsive UI with HTML, CSS & JavaScript

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Django
- Python

### Machine Learning
- TensorFlow / Keras
- Scikit-learn
- CNN
- Random Forest

### Database
- SQLite

### APIs
- OpenWeather API
- OpenRouter API

---

## 📂 Project Structure

```
AgroGuideAI/
│
├── Agro/
├── core/
│   ├── templates/
│   ├── ml/
│   ├── utils.py
│   └── views.py
│
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/anshi26-cyber/Agroguide-AI.git
cd Agroguide-AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

---

## 📸 Features Preview

- Home Page
- Crop Recommendation
- Plant Disease Detection
- AI Farming Assistant
- Weather Information
- User Profile

---

## 📊 Machine Learning Models

- Crop Recommendation Model
- Plant Disease Detection (CNN)
- Weather-based Prediction

> Large datasets and trained models are not included in this repository because of GitHub size limitations.

---

## 🔒 Environment Variables

Create a `.env` file.

```env
OPENROUTER_API_KEY=your_api_key
OPENWEATHER_API_KEY=your_api_key
SECRET_KEY=your_django_secret_key
```

---

## 👩‍💻 Author

**Anshika Kumari**

B.Tech CSE (AI & ML)

GitHub:
https://github.com/anshi26-cyber

---

## ⭐ If you like this project

Give this repository a ⭐ on GitHub.
