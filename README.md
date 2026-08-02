# 🌍 CO₂ AI Agent

> Generative AI Agent for Environmental CO₂ Reduction Awareness and Action Planning

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-red)
![Ollama](https://img.shields.io/badge/LLM-Llama3-green)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

CO₂ AI Agent is an AI-powered sustainability assistant developed as part of the **TCS Apex Capstone Project**.

The application estimates carbon emissions from user activities and provides AI-generated eco-friendly recommendations using Retrieval-Augmented Generation (RAG) with Llama 3.

Users can:

- Select an activity
- Describe an activity in natural language
- Upload a CSV dataset for AI analysis
- Visualize emissions through charts
- Download a PDF sustainability report

---

# ✨ Features

✅ Activity Selection from Dataset

✅ Natural Language Activity Analysis (RAG)

✅ CSV Upload & AI Dataset Analysis

✅ Carbon Emission Dashboard

✅ Daily / Monthly / Yearly Emission Calculation

✅ AI Sustainability Recommendations

✅ Download Analysis Report (PDF)

✅ Interactive Charts & Visualizations

---

# 🛠 Tech Stack

| Technology            | Purpose              |
| --------------------- | -------------------- |
| Python                | Backend              |
| Streamlit             | Web Interface        |
| Ollama (Llama 3)      | Large Language Model |
| ChromaDB              | Vector Database      |
| Sentence Transformers | Embedding Generation |
| LangChain             | RAG Workflow         |
| Pandas                | Data Processing      |
| Matplotlib            | Data Visualization   |
| ReportLab             | PDF Generation       |

---

# 🧠 AI Workflow

User Input

↓

Embedding Generation

↓

Vector Search (ChromaDB)

↓

Relevant Sustainability Tips Retrieved

↓

Llama 3 (Ollama)

↓

AI Recommendation

↓

Visualization & PDF Report

---

# 📂 Project Structure

```
CO2-AI-Agent
│
├── app.py
├── rag.py
├── embeddings.py
├── dataset.csv
├── tips.txt
├── requirements.txt
├── chroma_db/
└── README.md
```

---

# 📊 Visualizations

The application generates:

- Carbon Emission Summary
- Current vs Better Alternative
- Top 10 CO₂ Activities
- Category-wise CO₂ Distribution
- Category Summary Table

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/adarsha545/CO2-AI-Agent.git
```

Move inside project

```bash
cd CO2-AI-Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Ollama

```bash
ollama run llama3
```

Launch Streamlit

```bash
streamlit run app.py
```

---

# 📷 Screenshots

(Add screenshots here after deployment.)

Example:

- Home Page
- Activity Selection
- AI Recommendation
- CSV Upload
- Dashboard
- Charts

---

# 📈 Future Enhancements

- User Authentication
- Real-time Carbon API
- Voice Assistant
- Mobile Application
- Cloud Database
- Carbon Footprint Tracking

---

# 👨‍💻 Developer

**Adarsha Ghosh**

B.Tech in Computer Science & Engineering

TCS Apex Capstone Project 2026

GitHub:
https://github.com/adarsha545

---

# 📜 License

This project is developed for educational purposes under the TCS Apex Capstone Program.
