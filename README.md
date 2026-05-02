# 💰 SpendWell – Expense Tracker

SpendWell is a Streamlit-based web application designed to help users track their expenses, visualize spending habits, and gain insights to improve financial decisions.

---

## 🚀 Live Demo

👉 https://YOUR-APP-LINK.streamlit.app](https://spendwell-expense-tracker-jybzew6sayskzkoxd7x6eb.streamlit.app

---

## 📌 Features

### 🧾 Expense Management

* Add transactions with amount, category, date, and notes
* Delete transactions easily
* Persistent storage using SQLite database

### 📊 Data Visualization (Data Science Bonus)

* Total spending, average spending, and top category metrics
* Bar chart for spending by category
* Line chart for spending over time
* Trend analysis of user spending behavior

### 💡 Insights

* Identifies highest spending category
* Calculates total and average spending
* Provides simple recommendations to reduce expenses

### ⚙️ Customization

* Change currency (KD, USD, EUR, etc.)
* Add and edit categories with custom colors

### 🔍 Filtering & Search

* Search transactions by notes or category
* Filter by category
* Sort by date or amount

---

## 🏗️ Project Structure

```
spendwell-expense-tracker/
│
├── app.py          # Streamlit UI and main application logic
├── db.py           # Database operations (SQLite)
├── utils.py        # Data processing, analytics, and helper functions
├── requirements.txt
├── README.md
```

---

## 🗄️ Database Design

The app uses SQLite with three tables:

* **expenses**

  * id, amount, category, date, notes

* **categories**

  * id, name, color

* **settings**

  * key, value (used for currency)

---

## ⚙️ Installation (Run Locally)

```bash
git clone https://github.com/hashem8801/spendwell-expense-tracker.git
cd spendwell-expense-tracker
pip install -r requirements.txt
streamlit run app.py
```

---

## 🤖 AI Usage

AI tools (ChatGPT) were used to:

* Assist in structuring the project (modular design)
* Generate and refine parts of the UI logic
* Help implement data visualization and insights
* Debug errors and improve code clarity

All logic was reviewed, tested, and understood before final implementation.

---

## 📊 Data Science Bonus

The app includes a data analytics dashboard that:

* Aggregates spending by category
* Tracks spending trends over time
* Calculates key financial metrics
* Provides insight into user behavior

---

## 🎥 Demo / Walkthrough

👉 (Add your video link here)

---

## 🧠 What I Built Without AI

* Database schema
* Streamlit UI layout and navigation
* Filtering, sorting, and search functionality
* Integration between UI and database

---

## 📌 Future Improvements

* Budget tracking feature
* Real AI-based recommendations (ML model)
* User authentication

---

## 👤 Author

Hashim Fadhel AlSaba
Computer Engineering Student – Kuwait University

Hashim Fadhel Alsaba
Computer Engineering Student – Kuwait University
