# WeatherGPT

WeatherGPT

«An AI-powered weather assistant that combines real-time weather data with a conversational interface to make weather information easier to understand.»

📌 Overview

WeatherGPT is a web-based weather application designed to provide users with weather information through a simple, conversational interface.

The project uses Open-Meteo to obtain weather data and a FastAPI backend to handle API requests and connect the frontend with the weather service.

Instead of displaying only raw weather values, WeatherGPT is designed to present weather information in a more natural and user-friendly way.

---

✨ Features

- 🌤️ Real-time weather information
- 🌡️ Temperature and weather conditions
- 💨 Wind information
- 💧 Humidity and other weather parameters
- 📍 Location-based weather search
- 🤖 ChatGPT-style conversational interface
- ⚡ Fast API communication using FastAPI
- 🌐 Weather data provided by Open-Meteo
- 📱 Responsive web interface
- 🔄 Frontend and backend integration
- 🧩 Modular project structure

---

🛠️ Technologies Used

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- FastAPI
- Uvicorn
- HTTPX

Weather Data

- Open-Meteo

Development Tools

- Visual Studio Code
- Git
- GitHub

---

🏗️ Project Architecture

User
  │
  ▼
WeatherGPT Frontend
(HTML + CSS + JavaScript)
  │
  │ HTTP Request
  ▼
FastAPI Backend
(main.py)
  │
  │ API Request
  ▼
Open-Meteo
  │
  │ Weather Data
  ▼

Possible interface components include:

- Chat area
- User messages
- WeatherGPT responses
- Location input
- Weather information cards
- Loading indicators
- Error messages
- Responsive layout

---

🧪 Testing

Before using the application, verify:

- [ ] FastAPI server starts successfully
- [ ] Frontend loads correctly
- [ ] Backend endpoint responds
- [ ] Open-Meteo requests work
- [ ] Weather data appears correctly
- [ ] Invalid locations are handled
- [ ] Backend errors are handled
- [ ] API keys are not exposed
- [ ] ".env" is included in ".gitignore"

---

🐛 Troubleshooting

Backend is not starting

Make sure the required packages are installed:

pip install fastapi uvicorn httpx

Then start the server again:

uvicorn main:app --reload

Frontend cannot connect to backend

Check that the FastAPI server is running and that the frontend is using the correct backend URL.

For local development, it may look like:

http://127.0.0.1:8000

Weather data is not appearing

Check:

1. Internet connection
2. Browser console
3. FastAPI terminal output
4. Open-Meteo request
5. API endpoint URL
6. JSON response format

---

🚧 Future Improvements

Some possible future improvements include:

- 🤖 More advanced AI weather conversations
- 📍 Automatic location detection
- 🌧️ Rain prediction
- 📅 Extended weather forecasts
- 📊 Weather charts
- 🌡️ More detailed weather metrics
- 🌅 Sunrise and sunset information
- 🌎 Multiple location comparison
- 🎙️ Voice-based weather queries
- 📱 Improved mobile interface
- 🔔 Weather alerts
- 🧠 Personalized  
