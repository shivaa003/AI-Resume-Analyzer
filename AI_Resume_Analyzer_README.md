# 🤖 AI Resume Analyzer

An advanced AI-powered Resume Analyzer built using **Streamlit** and **Google Gemini AI**.  
Upload your resume and get intelligent insights, skill analysis, and job matching recommendations.

---

## 🚀 Features

- 📄 Upload Resume (PDF)
- 🔍 AI-powered Resume Analysis
- 🧠 Skill Assessment & Gap Analysis
- 💼 Job Description Matching
- 📊 Strengths & Weakness Detection
- 🎯 Personalized Improvement Suggestions
- 📚 Course Recommendations

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **AI Model:** Google Gemini (gemini-1.5-flash)
- **Libraries:**
  - pdfplumber
  - pytesseract
  - pdf2image
  - PIL
  - dotenv

---

## 📂 Project Structure

```
project/
│── app.py
│── .env
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

```bash
git clone <your-repo-link>
cd project
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file and add:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📌 How It Works

1. Upload your resume (PDF)
2. (Optional) Paste job description
3. Click **Analyze Resume**
4. Get detailed AI insights instantly

---

## 💡 Key Highlights

- Smart PDF text extraction (OCR fallback)
- Optimized token usage for API efficiency
- Retry mechanism for quota handling
- Clean & modern UI design

---

## ⚠️ Limitations

- API quota limits may apply
- OCR accuracy depends on PDF quality
- Large resumes may consume more tokens

---

## 🙌 Author

Developed by **Chandana Anumula**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
