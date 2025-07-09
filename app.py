import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_path
import pytesseract
import pdfplumber
import tempfile
import time

# Load environment variables
load_dotenv()

# Configure Google Gemini AI with error handling
def configure_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("❌ Google API key not found. Please set GOOGLE_API_KEY in your environment variables.")
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini AI: {str(e)}")
        return False

# Function to extract text from PDF with better error handling
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    text = ""
    
    try:
        # Try direct text extraction first
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    st.warning(f"⚠️ Failed to extract text from page {page_num + 1}: {str(e)}")
                    continue

        if text.strip():
            return text.strip()
            
    except Exception as e:
        st.warning(f"⚠️ Direct text extraction failed: {str(e)}")

    # Fallback to OCR for image-based PDFs
    st.info("📖 Falling back to OCR for image-based PDF...")
    try:
        images = convert_from_path(pdf_path, dpi=300)  # Higher DPI for better OCR
        for i, image in enumerate(images):
            try:
                page_text = pytesseract.image_to_string(image, lang='eng')
                if page_text.strip():
                    text += page_text + "\n"
            except Exception as e:
                st.warning(f"⚠️ OCR failed for page {i + 1}: {str(e)}")
                continue
                
    except Exception as e:
        st.error(f"❌ OCR processing failed: {str(e)}")
        return ""

    return text.strip()

# Function to check API quota status
def check_api_quota():
    try:
        # Test with a minimal request
        model = genai.GenerativeModel("gemini-1.5-flash")
        test_response = model.generate_content(
            "Test",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=10,
                temperature=0.1
            )
        )
        return True
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            return False
        return True

# Function to get response from Gemini AI with better quota management
def analyze_resume(resume_text, job_description=None, max_retries=2):
    if not resume_text or not resume_text.strip():
        return {"error": "Resume text is required for analysis."}
    
    # Check if resume text is too short
    if len(resume_text.strip()) < 50:
        return {"error": "Resume text appears to be too short. Please ensure the PDF contains readable text."}
    
    # Check API quota before processing
    if not check_api_quota():
        return {"error": "API quota exceeded. Please wait for quota reset or upgrade your plan. Check: https://ai.google.dev/gemini-api/docs/rate-limits"}
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Optimize prompt to reduce token usage
        base_prompt = f"""
        As an HR expert, analyze this resume and provide:
        1. Skills assessment
        2. Strengths & weaknesses
        3. Improvement suggestions
        4. Course recommendations

        Resume: {resume_text[:3000]}...
        """

        if job_description and job_description.strip():
            base_prompt += f"""
            
            Job Description: {job_description[:1000]}...
            
            Additional analysis:
            - Match percentage
            - Role-specific gaps
            - Targeted recommendations
            """

        # Retry logic with longer delays for quota issues
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    base_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.8,
                        top_k=40,
                        max_output_tokens=1500,  # Reduced to save quota
                    )
                )
                
                if response and response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response from Gemini AI")
                    
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        st.warning(f"⚠️ Quota limit reached. Waiting 30 seconds before retry...")
                        time.sleep(30)  # Longer wait for quota issues
                        continue
                    else:
                        return {"error": "API quota exceeded. Please try again later or upgrade your plan."}
                elif attempt < max_retries - 1:
                    st.warning(f"⚠️ API call failed (attempt {attempt + 1}/{max_retries}): {error_str}")
                    time.sleep(5)  # Standard retry delay
                    continue
                else:
                    raise e

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return {"error": "API quota exceeded. Please try again later or check your API limits. Visit: https://ai.google.dev/gemini-api/docs/rate-limits"}
        elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
            return {"error": "Invalid API key. Please check your Google API key configuration."}
        elif "permission" in error_msg.lower():
            return {"error": "Permission denied. Please check your API key permissions."}
        else:
            return {"error": f"Analysis failed: {error_msg}"}

# Custom CSS (keeping your existing styling)
def inject_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Root variables */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #1e40af;
        --accent-color: #60a5fa;
        --text-primary: #ffffff;
        --text-secondary: #cbd5e1;
        --background: #000000;
        --card-bg: #1a1a1a;
        --border-color: #374151;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
    }
    
    /* Hide Streamlit default elements */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        background: var(--background);
        font-family: 'Poppins', sans-serif;
        color: var(--text-primary);
    }
    
    /* Main container */
    .main-container {
        background: var(--card-bg);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        position: relative;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    .main-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    /* Header styling */
    .custom-header {
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .custom-header h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .custom-header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #3b82f620, #1e40af20);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px dashed var(--primary-color);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .upload-section:hover {
        border-color: var(--accent-color);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }
    
    .upload-icon {
        font-size: 3rem;
        color: var(--primary-color);
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Job description section */
    .job-section {
        background: linear-gradient(135deg, #60a5fa20, #3b82f620);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 4px solid var(--accent-color);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 12px 30px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, var(--secondary-color), var(--accent-color));
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Alert styling */
    .alert {
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #48bb7820, #38a16920);
        color: var(--success-color);
        border-left: 4px solid var(--success-color);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ed893620, #dd6b2020);
        color: var(--warning-color);
        border-left: 4px solid var(--warning-color);
    }
    
    .alert-error {
        background: linear-gradient(135deg, #f5656520, #e53e3e20);
        color: var(--error-color);
        border-left: 4px solid var(--error-color);
    }
    
    /* Results section */
    .results-section {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Custom footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
        color: var(--text-secondary);
    }
    
    .custom-footer a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .custom-footer a:hover {
        color: var(--secondary-color);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .custom-header h1 {
            font-size: 2rem;
        }
        
        .main-container {
            margin: 1rem;
            padding: 1rem;
        }
        
        .upload-section, .job-section {
            padding: 1rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Streamlit app
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Inject custom CSS
inject_custom_css()

# Check API configuration
if not configure_gemini():
    st.stop()

# Custom HTML structure
st.markdown("""
<div class="main-container">
    <div class="custom-header">
        <h1>🤖 AI Resume Analyzer</h1>
        <p>Analyze your resume and match it with job descriptions using advanced AI technology</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="upload-section">
        <div style="text-align: center;">
            <div class="upload-icon">📄</div>
            <h3 style="color: var(--primary-color); margin-bottom: 1rem;">Upload Your Resume</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Drop your PDF file here or click to browse</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["pdf"], key="resume_upload")

with col2:
    st.markdown("""
    <div class="job-section">
        <h3 style="color: var(--accent-color); margin-bottom: 1rem;">💼 Job Description</h3>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">Paste the job description to get targeted analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    job_description = st.text_area("", placeholder="Paste the job description here...", height=200, key="job_desc")

# Status messages
if uploaded_file is not None:
    st.markdown("""
    <div class="alert alert-success">
        <span>✅</span>
        <span>Resume uploaded successfully! Ready for analysis.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="alert alert-warning">
        <span>⚠️</span>
        <span>Please upload a resume in PDF format to continue.</span>
    </div>
    """, unsafe_allow_html=True)

# Analysis section
st.markdown("<div style='padding: 2rem 0;'></div>", unsafe_allow_html=True)

if uploaded_file:
    # Add quota status check
    st.markdown("""
    <div style="background: linear-gradient(135deg, #60a5fa20, #3b82f620); 
               border-radius: 10px; padding: 1rem; margin: 1rem 0; 
               border-left: 4px solid var(--accent-color);">
        <p style="color: var(--text-secondary); margin: 0;">
            💡 <strong>Tip:</strong> Large resumes may consume more API quota. 
            Consider using shorter job descriptions to optimize usage.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the analyze button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 Analyze Resume", use_container_width=True)
    
    if analyze_button:
        # Use temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        
        try:
            # Show loading animation
            with st.spinner("🔄 Extracting text from PDF..."):
                resume_text = extract_text_from_pdf(tmp_file_path)
            
            if not resume_text:
                st.error("❌ Failed to extract text from the PDF. Please ensure the file contains readable text.")
            else:
                # Show analysis progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔄 Analyzing resume with AI...")
                progress_bar.progress(25)
                
                # Analyze resume
                analysis = analyze_resume(resume_text, job_description)
                progress_bar.progress(75)
                
                # Check if analysis returned an error
                if isinstance(analysis, dict) and "error" in analysis:
                    st.error(f"❌ {analysis['error']}")
                else:
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis completed successfully!")
                    
                    # Display results
                    st.markdown("""
                    <div class="results-section">
                        <h2 style="color: var(--primary-color); margin-bottom: 1.5rem;">📊 Analysis Results</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff, #f8f9fa); 
                               border-radius: 15px; padding: 2rem; margin: 1rem 0; 
                               border: 1px solid var(--border-color); 
                               box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                        <div style="white-space: pre-wrap; line-height: 1.6; color: #333;">
                            {analysis}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.analysis_complete = True
                
                # Clean up progress indicators
                progress_bar.empty()
                status_text.empty()
                
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass

# Custom footer
st.markdown("""
<div class="custom-footer">
    <p>Powered by <strong>Streamlit</strong> and <strong>Google Gemini AI</strong> | 
    Developed by <strong>Chandana Anumula</strong></p>
</div>
""", unsafe_allow_html=True)