# AI Hiring Intelligence System 🚀
.
An AI-powered hiring assistant that analyzes candidate resumes against job descriptions and calculates a compatibility score using Natural Language Processing (NLP).

This system simulates how modern Applicant Tracking Systems (ATS) help recruiters quickly evaluate candidates by analyzing resumes, estimating experience, and ranking applicants based on relevance to a job description..

---

## 📌 Features.

* AI-powered resume and job description matching
* TF-IDF based Natural Language Processing
* Cosine Similarity scoring system
* Automatic experience extraction from resumes
* Candidate ranking system
* Backend API built with FastAPI
* Interactive frontend built with Streamlit
* Database storage using SQLAlchemy

---

## 🧠 How the AI Works.

The system uses **Natural Language Processing techniques** to compare resumes with job descriptions.

1. Text preprocessing cleans the input data.
2. TF-IDF converts text into numerical vectors.
3. Cosine similarity measures how closely the resume matches the job description.
4. Regex pattern matching extracts candidate experience.
5. Results are stored in a database for recruiter review.

---

## 🏗 System Architecture

Frontend (Streamlit UI)
↓
FastAPI Backend
↓
AI Engine (TF-IDF + Cosine Similarity)
↓
Database (SQLAlchemy)

---

## 🛠 Technologies Used

Python
FastAPI
Streamlit
Scikit-learn
SQLAlchemy
Pydantic
Regex
Uvicorn

---

## 📂 Project Structure

ai-hiring-system

backend/

* main.py
* ai_engine.py
* database.py

frontend/

* streamlit_app.py

requirements.txt
README.md

---

## ⚙️ Installation

Clone the repository

git clone https://github.com/Allankw-dev/ai-hiring-system.git

Navigate into the project

cd ai-hiring-system

Install dependencies

pip install -r requirements.txt

---

## ▶️ Running the Backend

Start the FastAPI server

uvicorn backend.main:app --reload

The API will run at

http://127.0.0.1:8000

---

## ▶️ Running the Frontend

Start the Streamlit application

streamlit run frontend/streamlit_app.py

---

## 📡 API Endpoints

GET /

Returns system status.

POST /analyze

Analyzes a candidate resume against a job description.

GET /candidates

Returns stored candidates and their match scores.

---

## 📊 Example Response

{
"name": "John Doe",
"match_score": 84.3,
"experience": 3
}

---

## 🚀 Future Improvements

* Skill extraction using NLP
* Machine learning based candidate ranking
* Resume PDF parsing
* Job skill detection
* Candidate dashboard
* Docker deployment

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Allan Kamau
GitHub: https://github.com/Allankw-dev

---

⭐ If you found this project useful, consider giving it a star.
