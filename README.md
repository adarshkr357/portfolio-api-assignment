# 🧠 Portfolio Website Generator API – Backend Developer Assignment

This project provides a set of modular APIs for:
- Parsing resumes and generating structured website JSON
- Translating content into multiple languages
- Converting currency prices based on user preference

---

## 🚀 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML + JS (basic testing interface)
- **Libraries**: flask-cors, requests, PyPDF2, python-docx

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/adarshkr357/portfolio-api-assignment.git
cd portfolio-api-assignment
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

### 3. Run the Flask App

```bash
python app.py
```

App runs on: `http://localhost:5000`

---

## 📁 API Endpoints

### 🔹 1. Resume Parser

**POST** `/api/parse-resume`

* **Form Data**: `file` (PDF or DOC/DOCX)
* **Response**:

```json
{
  "success": true,
  "data": {
    "hero": { "name": "...", "bio": "..." },
    "about": { "description": "..." },
    "skills": [...],
    "experience": [...],
    "education": [...],
    "contact": { "email": "...", "phone": "..." }
  }
}
```

---

### 🔹 2. Text Translator

**POST** `/api/translate`

* **JSON**:

```json
{
  "text": "Hello World",
  "target_language": "fr"
}
```

* **Response**:

```json
{
  "success": true,
  "translated": "Bonjour le monde"
}
```

---

### 🔹 3. Currency Converter

**POST** `/api/currency/convert`

* **JSON**:

```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "INR"
}
```

* **Response**:

```json
{
  "success": true,
  "converted_amount": 8325.45,
  "exchange_rate": 83.25
}
```

---

## 🧪 Testing Interface

* Visit [http://localhost:5000](http://localhost:5000) after running the app.
* Upload resume, translate text, and convert currency using the simple frontend UI.

---

## 🌐 CORS Support

Flask-CORS is enabled, making this API ready for integration with React or other frontend frameworks.
