"""
Medical Report Analyzer - Flask Backend API
Handles file uploads, AI analysis, and result serving
"""

import os
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
# transformers imported conditionally if available
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize AI model (using a text classification/summarization model)
classifier = None
summarizer = None
try:
    from transformers import pipeline
    # Using a text analysis pipeline for medical report analysis
    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # CPU
    )
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=-1  # CPU
    )
    logger.info("AI models loaded successfully")
except ImportError as e:
    logger.warning(f"Transformers not available, running without AI models: {e}")
    classifier = None
    summarizer = None
except Exception as e:
    logger.warning(f"Error loading AI models, running in basic mode: {e}")
    classifier = None
    summarizer = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting PDF: {e}")
        return ""


def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading TXT file: {e}")
        return ""


def analyze_medical_report(text):
    """
    Analyze medical report text using AI models
    Returns analysis results with health indicators
    """
    if not text or len(text.strip()) < 10:
        return {
            "error": "Text too short to analyze"
        }
    
    # Medical keywords to check
    medical_keywords = {
        'glucose': {'keywords': ['glucose', 'blood sugar', 'glu'], 'normal_range': (70, 100)},
        'hemoglobin': {'keywords': ['hemoglobin', 'hgb', 'hb'], 'normal_range': (12, 17)},
        'cholesterol': {'keywords': ['cholesterol', 'chol', 'ldl', 'hdl'], 'normal_range': (0, 200)},
        'blood_pressure': {'keywords': ['blood pressure', 'bp', 'systolic', 'diastolic'], 'normal_range': (90, 140)},
        'rbc': {'keywords': ['red blood cell', 'rbc', 'erythrocyte'], 'normal_range': (4.5, 6.0)},
        'wbc': {'keywords': ['white blood cell', 'wbc', 'leukocyte'], 'normal_range': (4000, 11000)},
        'platelets': {'keywords': ['platelet', 'plt'], 'normal_range': (150000, 450000)},
    }
    
    # Extract numeric values from text
    findings = {}
    text_lower = text.lower()
    
    # Try to extract values using regex
    for condition, info in medical_keywords.items():
        for keyword in info['keywords']:
            if keyword in text_lower:
                # Look for numeric values near the keyword
                pattern = rf'{keyword}[:\s]*([\d.]+)'
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    try:
                        value = float(matches[0])
                        normal_range = info['normal_range']
                        status = "normal"
                        if value < normal_range[0]:
                            status = "low"
                        elif value > normal_range[1]:
                            status = "high"
                        
                        findings[condition] = {
                            "value": value,
                            "normal_range": normal_range,
                            "status": status,
                            "keyword": keyword
                        }
                        break
                    except ValueError:
                        continue
    
    # Use AI model for text analysis if available
    analysis_summary = ""
    risk_level = "low"
    
    if summarizer:
        try:
            # Summarize the report (truncate to model max length)
            text_for_summary = text[:1024] if len(text) > 1024 else text
            summary = summarizer(text_for_summary, max_length=150, min_length=30, do_sample=False)
            analysis_summary = summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Error in summarization: {e}")
            analysis_summary = "Unable to generate AI summary"
    else:
        analysis_summary = "AI summarization model not available"
    
    # Determine overall risk level
    high_risk_count = sum(1 for f in findings.values() if f['status'] == 'high' or f['status'] == 'low')
    if high_risk_count >= 3:
        risk_level = "high"
    elif high_risk_count >= 1:
        risk_level = "moderate"
    else:
        risk_level = "low"
    
    return {
        "summary": analysis_summary,
        "findings": findings,
        "risk_level": risk_level,
        "analysis_date": datetime.now().isoformat(),
        "text_length": len(text)
    }


@app.route('/')
def index():
    """Serve frontend index page"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "medical-report-analyzer",
        "models_loaded": classifier is not None and summarizer is not None
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF and TXT files are allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.info(f"File uploaded: {filename}")
        
        # Extract text based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_txt(file_path)
        
        if not text or len(text.strip()) < 10:
            return jsonify({"error": "Could not extract meaningful text from file"}), 400
        
        # Analyze the report
        analysis = analyze_medical_report(text)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Could not delete file: {e}")
        
        return jsonify({
            "success": True,
            "filename": filename,
            "analysis": analysis
        })
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze medical report text directly"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    
    if len(text.strip()) < 10:
        return jsonify({"error": "Text too short to analyze"}), 400
    
    try:
        analysis = analyze_medical_report(text)
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

