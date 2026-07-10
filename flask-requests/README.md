# 💱 Currency Converter - Flask App

A simple web app that converts currencies using live exchange rates via ExchangeRate-API and Flask.

---

## 📌 Features

- Converts currency using real-time rates
- Built using Python Flask
- Clean UI using HTML & CSS
- No JS required

---

## 🧰 Steps to Build

### 1. Get Your API Key

- Go to [https://www.exchangerate-api.com](https://www.exchangerate-api.com)
- Sign up for a free account
- Copy your API Key (example: `2666e8f90d333912962dcf12a6`)

---

### 2. Set Up the Project

Create your project folder:

```bash
mkdir currency-converter && cd currency-converter
```

---

### 3. Create Virtual Environment

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
```

---

### 4. Install Flask and Requests

```bash
pip install flask requests
```

(Optional: save dependencies)

```bash
pip freeze > requirements.txt
```

---

### 5. Create the Files

Create these:

- `app.py` – main Flask application
- `converter.py` – handles API call
- `templates/index.html` – HTML form and result
- `static/style.css` – styling

---

### 6. Add Your API Key

Inside `converter.py`, replace:

```
API_KEY = "25e8f90d66664333912962dcf12ae"
```

with your real key.

---

### 7. Run the App

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## ✅ Example

Input:

- Amount: `100`
- From: `USD`
- To: `EUR`

Output:

> ✅ Result: 93.57

---

## 👨‍💻 Author

**Souhail Segni**  
GitLab | LinkedIn | Email

---

## 📝 Notes

- Make sure `templates/index.html` and `static/style.css` are in the correct folders.
- App runs in development mode — don’t use in production without proper WSGI config.