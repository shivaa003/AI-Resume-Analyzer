** AI-Powered Resume Analyzer**

Meet the AI-Powered Resume Analyzer — an intelligent assistant built to replicate the skills of a seasoned HR professional. Powered by Google Generative AI (Gemini), this application smartly evaluates resumes, assesses job relevance, and provides customized feedback to improve your career prospects.

🧩 Project Summary
The AI-Powered Resume Analyzer acts as a personal career consultant and resume screener, offering:

->A comprehensive breakdown of resume content.

->Insights into your strengths and areas of improvement.

->Skill development suggestions tailored to your goals.

->Resume-job alignment checks for specific job roles.

It’s an essential tool for both job seekers aiming to improve their resumes and recruiters seeking faster screening processes.

🌟 Key Functionalities
🔍 1. General Resume Review
Delivers a one-line summary of your resume.

Extracts and displays your current skill set.

Detects missing or weak skills and recommends enhancements.

Recommends relevant and trending online courses.

Provides a holistic overview of your strengths and weaknesses.

🎯 2. Job-Specific Resume Compatibility
Compares your resume against a job description.

Calculates a match score (in %) for compatibility.

Lists essential skills missing from your profile.

Advises on resume readiness or improvement needs for the role.

## 🧪 Technology Stack

| **Component**         | **Technology Used**                                                   |
|-----------------------|------------------------------------------------------------------------|
| Frontend Interface     | Streamlit – for building an interactive user experience               |
| Backend Language       | Python – for handling logic and data processing                       |
| AI Engine              | Google Gemini – for natural language understanding                    |
| PDF Text Extraction    | pdfplumber – for structured text extraction                           |
| OCR Backup             | pytesseract – fallback for image-based PDFs                           |
| Security               | .env files – for managing sensitive API keys securely                 |


⚙️ How the System Operates
1.Extracting Resume Content

2.Upload a resume in PDF format. The app pulls the text using pdfplumber or OCR if needed.

3.Processing Through AI

4.Google Gemini processes the resume, extracts insights, summarizes content, and evaluates it based on the job description (if provided).

5.Delivering Insights

6.You receive a breakdown of strengths, skill gaps, and course recommendations.

7.A match percentage is displayed when a job description is included.



🤝 Contributions Welcome
Want to improve the project or add features?

>Fork the repository on GitHub.

>Create a feature branch with your updates.

>Submit a pull request with a clear explanation of your contribution.

Let’s build smarter career tools together!