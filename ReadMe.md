# CarScan AI: AI-powered Car Brand Detection

CarScan AI is a web application that identifies car brands from images. The backend runs with FastAPI, and the frontend is a responsive HTML/Tailwind interface for uploading images and seeing predictions.

---

## Requirements

- Python 3.10+
- Modern web browser (Chrome, Edge, Firefox, etc.)
- VS Code with **Live Server** extension

---

## Setup Instructions

### 1. Install Python

Download and install Python from [python.org](https://www.python.org/downloads/).  
Ensure `python` and `pip` are available in your system PATH.

### 2. Install dependencies

Open a terminal in the `./backend/` folder and run:

```bash
pip install -r requirements.txt
```

This will install all necessary packages including `torch`, `torchvision`, `Pillow`, `fastapi`, and others.

### 3. Run the backend server

From the `./backend/` folder, run:

```bash
uvicorn main:app --reload
```

- The FastAPI server will start at `http://127.0.0.1:8000`.
- It will automatically reload when you change Python files.

### 4. Run the frontend

Open `index.html` with **Live Server** in VS Code:

- Right-click `index.html` → **Open with Live Server**
- The frontend communicates automatically with the backend for predictions.

---

## Usage

1. Click **Try with Your Own Image** to select a car image.
2. The backend will predict the car brand and display confidence.
3. Results are shown directly on the frontend in a formatted panel.

---

## Notes

- Ensure the backend is running before submitting images from the frontend.
- Backend is configured with CORS to allow all origins for local testing.

---
