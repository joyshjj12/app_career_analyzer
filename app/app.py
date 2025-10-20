# from flask import Flask, request, render_template, redirect, url_for, session
# import fitz
# import google.generativeai as genai
# import json
# import os # Import os for setting up secret key

# app = Flask(__name__)
# # Use a secret key for session management (required for flash messages/sessions)
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_dev') 

# # IMPORTANT: Use your actual key (consider using environment variables in production)
# genai.configure(api_key="AIzaSyBqBqJnskZx-YdurWWsoZ2cDLy7vdq_GE8")

# # In-memory storage for analysis results (replace with a database for a real app)
# analysis_data_store = {}

# # Helper function for PDF text extraction (same as original)
# def extract_text(file):
#     """Extracts text from a PDF file object using fitz/PyMuPDF."""
#     pdf = fitz.open(stream=file.read(), filetype="pdf")
#     text = ""
#     for page in pdf:
#         text += page.get_text()
#     return text

# @app.route('/')
# def home():
#     """Renders the main upload/home page."""
#     # Clears any old analysis session data
#     session.pop('analysis_id', None) 
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze_resume():
#     """Handles file upload, calls Gemini, and stores results."""
#     if 'resume' not in request.files:
#         return redirect(url_for('home'))

#     file = request.files['resume']
#     if file.filename == '':
#         return redirect(url_for('home'))
        
#     text = extract_text(file)
#     model = genai.GenerativeModel("models/gemini-2.5-pro")

#     # COMBINED PROMPT: Asking for all data in a single, complex JSON structure
#     prompt = f"""
#     Analyze the following resume text. Output your response as a single, valid, raw JSON object, and nothing else.
    
#     The JSON structure MUST be exactly this. Provide an explanation for every list item.
#     {{
#         "overall_score": 0,
#         "score_reason": "",
#         "summary_rewrite": "",
#         "key_skills": [],
#         "ats_risks": [], // 3 potential risks
#         "ats_improvements": [], // 3 suggestions to improve ATS score
#         "predicted_roles": [ // Top 3 roles with explanations
#             {{"title": "", "explanation": ""}},
#             {{"title": "", "explanation": ""}},
#             {{"title": "", "explanation": ""}}
#         ],
#         "detailed_suggestions": "" // Comprehensive suggestions for overall improvement
#     }}
    
#     For "overall_score", rate the resume out of 100 based on quality and best practices.
#     For "summary_rewrite", write a concise, high-impact professional summary (4-5 sentences max).
    
#     Resume Text:
#     {text}
#     """
    
#     analysis_id = str(hash(text)) # Simple unique ID based on the resume content
    
#     try:
#         response = model.generate_content(prompt)
#         raw_json_string = response.text.strip()
        
#         # Cleanup logic for models that wrap JSON in backticks
#         if raw_json_string.startswith("```json"):
#             raw_json_string = raw_json_string.strip("```json").strip("```").strip()

#         results_data = json.loads(raw_json_string)
        
#         # Store data and redirect to the analysis report
#         analysis_data_store[analysis_id] = results_data
#         session['analysis_id'] = analysis_id
#         return redirect(url_for('show_analysis', report_id=analysis_id))

#     except Exception as e:
#         print(f"Error during Gemini analysis (JSON parsing failed): {e}")
#         # Placeholder data for error case
#         error_data = {
#             "overall_score": "Error", 
#             "score_reason": f"Analysis failed: {e}",
#             "summary_rewrite": "N/A",
#             "key_skills": ["N/A"],
#             "ats_risks": ["N/A"],
#             "ats_improvements": ["N/A"],
#             "predicted_roles": [{"title": "N/A", "explanation": "Error"}], 
#             "detailed_suggestions": "An error occurred during analysis. Please check the resume data."
#         }
#         analysis_data_store[analysis_id] = error_data
#         session['analysis_id'] = analysis_id
#         return redirect(url_for('show_analysis', report_id=analysis_id))

# @app.route('/report/<report_id>')
# def show_analysis(report_id):
#     """Renders the analysis report with navigation."""
#     data = analysis_data_store.get(report_id)
#     if not data:
#         return redirect(url_for('home')) # Redirect home if ID is invalid
    
#     return render_template('results.html', data=data)

# if __name__ == '__main__':
#     # Changed port for common usage
#     app.run(host='0.0.0.0', debug=True, port=8000)


# from flask import Flask, request, render_template, redirect, url_for, session, jsonify # ADDED jsonify
# import fitz
# import google.generativeai as genai
# import json
# import os 

# app = Flask(__name__)
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_dev') 

# # IMPORTANT: Use your actual key
# genai.configure(api_key="AIzaSyBqBqJnskZx-YdurWWsoZ2cDLy7vdq_GE8")

# # In-memory storage for analysis results (replace with a database for a real app)
# analysis_data_store = {}

# # Helper function for PDF text extraction (same as original)
# def extract_text(file):
#     """Extracts text from a PDF file object using fitz/PyMuPDF."""
#     pdf = fitz.open(stream=file.read(), filetype="pdf")
#     text = ""
#     for page in pdf:
#         text += page.get_text()
#     return text

# @app.route('/')
# def home():
#     """Renders the main upload/home page."""
#     session.pop('analysis_id', None) 
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze_resume():
#     """Handles file upload, calls Gemini, and stores results."""
#     # ... (Keep the existing analysis logic as it is correct) ...
#     if 'resume' not in request.files:
#         return redirect(url_for('home'))

#     file = request.files['resume']
#     if file.filename == '':
#         return redirect(url_for('home'))
        
#     text = extract_text(file)
#     model = genai.GenerativeModel("models/gemini-2.5-pro")

#     prompt = f"""
#     Analyze the following resume text. Output your response as a single, valid, raw JSON object, and nothing else.
    
#     The JSON structure MUST be exactly this. Provide an explanation for every list item.
#     {{
#         "overall_score": 0,
#         "score_reason": "",
#         "summary_rewrite": "",
#         "key_skills": [],
#         "ats_risks": [], 
#         "ats_improvements": [],
#         "predicted_roles": [ 
#             {{"title": "", "explanation": ""}},
#             {{"title": "", "explanation": ""}},
#             {{"title": "", "explanation": ""}}
#         ],
#         "detailed_suggestions": ""
#     }}
    
#     For "overall_score", rate the resume out of 100 based on quality and best practices.
#     For "summary_rewrite", write a concise, high-impact professional summary (4-5 sentences max).
    
#     Resume Text:
#     {text}
#     """
    
#     analysis_id = str(hash(text))
    
#     try:
#         response = model.generate_content(prompt)
#         raw_json_string = response.text.strip()
        
#         if raw_json_string.startswith("```json"):
#             raw_json_string = raw_json_string.strip("```json").strip("```").strip()

#         results_data = json.loads(raw_json_string)
        
#         analysis_data_store[analysis_id] = results_data
#         session['analysis_id'] = analysis_id
#         return redirect(url_for('show_analysis', report_id=analysis_id))

#     except Exception as e:
#         print(f"Error during Gemini analysis (JSON parsing failed): {e}")
#         error_data = {
#             "overall_score": "Error", 
#             "score_reason": f"Analysis failed: {e}",
#             "summary_rewrite": "N/A",
#             "key_skills": ["N/A"],
#             "ats_risks": ["N/A"],
#             "ATS_improvements": ["N/A"],
#             "predicted_roles": [{"title": "N/A", "explanation": "Error"}], 
#             "detailed_suggestions": "An error occurred during analysis. Please check the resume data."
#         }
#         analysis_data_store[analysis_id] = error_data
#         session['analysis_id'] = analysis_id
#         return redirect(url_for('show_analysis', report_id=analysis_id))


# # -----------------------------------------------------------
# # CRITICAL FIXES START HERE
# # -----------------------------------------------------------

# @app.route('/report/<report_id>')
# def show_analysis(report_id):
#     """Renders the main SPA wrapper (HTML shell)."""
#     data = analysis_data_store.get(report_id)
#     if not data:
#         return redirect(url_for('home')) 
    
#     # Renders the HTML template that contains the JavaScript for SPA navigation.
#     # The name must match the HTML file:
#     return render_template('analysis_spa.html', report_id=report_id, initial_data=data)


# @app.route('/report/<report_id>/data')
# def get_analysis_data(report_id):
#     """NEW API ENDPOINT: Serves the raw JSON data to the JavaScript fetch call."""
#     data = analysis_data_store.get(report_id)
#     if not data:
#         # Returns a 404 error if the analysis ID is no longer in memory
#         return jsonify({"error": "Report not found"}), 404 
    
#     # Returns the stored Python dictionary as JSON data
#     return jsonify(data) 


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=8000)


from flask import Flask, request, render_template, redirect, url_for, session, jsonify, send_file, Response
import fitz
import google.generativeai as genai
import json
import os 

from io import BytesIO # NEW: For serving the PDF file in memory

# --- Configuration ---
app = Flask(__name__)
# Use a secret key for session management
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_dev') 

# IMPORTANT: Use your actual key
genai.configure(api_key="AIzaSyBqBqJnskZx-YdurWWsoZ2cDLy7vdq_GE8")

# In-memory storage for analysis results
analysis_data_store = {}

# --- PDFKIT CONFIGURATION ---
# Uncomment and adjust this line if 'wkhtmltopdf' is NOT in your system's PATH
# config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
config = None # Keep this line if wkhtmltopdf is configured on your system PATH

# --- Helper Functions ---

def extract_text(file):
    """Extracts text from a PDF file object using fitz/PyMuPDF."""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def generate_modified_resume_html(data):
    """
    Creates a simple, clean HTML representation of a resume using
    the analysis data, prioritizing the AI suggestions, for PDF conversion.
    """
    score = data.get('overall_score', 'N/A')
    summary = data.get('summary_rewrite', 'N/A')
    suggestions = data.get('detailed_suggestions', 'N/A')
    key_skills = data.get('key_skills', [])

    # The HTML template is simple and robust for PDF conversion
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Modified Resume Draft</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1 {{ border-bottom: 2px solid #0077b6; padding-bottom: 5px; color: #0077b6; }}
            h2 {{ color: #333; margin-top: 20px; }}
            .section {{ margin-bottom: 25px; padding: 10px; border-left: 5px solid #ff9900; background: #f9f9f9; }}
            .score-box {{ text-align: right; font-size: 2em; color: #0077b6; font-weight: bold; }}
            ul {{ list-style-type: disc; margin-left: 20px; }}
            pre {{ white-space: pre-wrap; background: #eee; padding: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="score-box">AI Score: {score}/100</div>
        <h1>AI Resume Analysis Report Summary</h1>
        
        <div class="section">
            <h2>Professional Summary (AI Rewrite)</h2>
            <p>{summary}</p>
        </div>

        <div class="section">
            <h2>Key Skills</h2>
            <ul>
                {''.join(f'<li>{skill}</li>' for skill in key_skills)}
            </ul>
        </div>

        <div class="section">
            <h2>Detailed Improvement Suggestions</h2>
            <pre>{suggestions}</pre>
        </div>

        <div class="section">
            <h2>Predicted Roles</h2>
            <ul>
                {''.join(f'<li><strong>{role["title"]}</strong>: {role["explanation"]}</li>' for role in data.get('predicted_roles', []))}
            </ul>
        </div>
        
    </body>
    </html>
    """
    return html_content

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main upload/home page."""
    session.pop('analysis_id', None) 
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Handles file upload, calls Gemini, and stores results."""
    if 'resume' not in request.files:
        return redirect(url_for('home'))

    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('home'))
        
    text = extract_text(file)
    model = genai.GenerativeModel("models/gemini-2.5-pro")

    prompt = f"""
    Analyze the following resume text. Output your response as a single, valid, raw JSON object, and nothing else.
    
    The JSON structure MUST be exactly this. Provide an explanation for every list item.
    {{
        "overall_score": 0,
        "score_reason": "",
        "summary_rewrite": "",
        "key_skills": [],
        "ats_risks": [], 
        "ats_improvements": [],
        "predicted_roles": [ 
            {{"title": "", "explanation": ""}},
            {{"title": "", "explanation": ""}},
            {{"title": "", "explanation": ""}}
        ],
        "detailed_suggestions": ""
    }}
    
    For "overall_score", rate the resume out of 100 based on quality and best practices.
    For "summary_rewrite", write a concise, high-impact professional summary (4-5 sentences max).
    
    Resume Text:
    {text}
    """
    
    analysis_id = str(hash(text))
    
    try:
        response = model.generate_content(prompt)
        raw_json_string = response.text.strip()
        
        if raw_json_string.startswith("```json"):
            raw_json_string = raw_json_string.strip("```json").strip("```").strip()

        results_data = json.loads(raw_json_string)
        print("\n--- DEBUG: ATS RISKS STRUCTURE ---")
        print(results_data.get('ats_risks'))
        print("----------------------------------\n")
        analysis_data_store[analysis_id] = results_data
        session['analysis_id'] = analysis_id
        return redirect(url_for('show_analysis', report_id=analysis_id))

    except Exception as e:
        print(f"Error during Gemini analysis (JSON parsing or API issue): {e}")
        error_data = {
            "overall_score": "Error", 
            "score_reason": f"Analysis failed: {e}",
            "summary_rewrite": "N/A",
            "key_skills": ["N/A"],
            "ats_risks": ["N/A"],
            "ats_improvements": ["N/A"],
            "predicted_roles": [{"title": "N/A", "explanation": "Error"}], 
            "detailed_suggestions": "An error occurred during analysis. Please check the server console for details."
        }
        analysis_data_store[analysis_id] = error_data
        session['analysis_id'] = analysis_id
        return redirect(url_for('show_analysis', report_id=analysis_id))


@app.route('/report/<report_id>')
def show_analysis(report_id):
    """Renders the main SPA wrapper (HTML shell)."""
    data = analysis_data_store.get(report_id)
    if not data:
        return redirect(url_for('home')) 
    
    # Renders the HTML template that contains the JavaScript for SPA navigation.
    return render_template('results.html', report_id=report_id)


@app.route('/report/<report_id>/data')
def get_analysis_data(report_id):
    """API ENDPOINT: Serves the raw JSON data to the JavaScript fetch call."""
    data = analysis_data_store.get(report_id)
    if not data:
        return jsonify({"error": "Report not found"}), 404 
    
    return jsonify(data) 


from flask import Flask, request, render_template, redirect, url_for, session, jsonify, send_file, Response # Keep Response
# REMOVE: from weasyprint import HTML

# ADD ReportLab Imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO 
# Note: BytesIO is used to hold the PDF data in memory
# ReportLab helper function to generate the PDF content
def generate_reportlab_pdf(data):
    """
    Generates the PDF content using ReportLab's drawing commands.
    This replaces the HTML generation helper function.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, 
                            rightMargin=inch/2, 
                            leftMargin=inch/2,
                            topMargin=inch/2, 
                            bottomMargin=inch/2)
    
    styles = getSampleStyleSheet()
    
    # Define Custom Styles for the Report
    styles.add(ParagraphStyle(name='CustomHeading1', fontSize=18, spaceAfter=10, 
                              textColor=colors.HexColor('#0077b6'), alignment=1)) # Center
    styles.add(ParagraphStyle(name='CustomHeading2', fontSize=14, spaceBefore=10, 
                          textColor=colors.black, spaceAfter=5, 
                          fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='CustomBodyText', fontSize=10, spaceAfter=5))
    styles.add(ParagraphStyle(name='CustomRiskItem', fontSize=10, spaceAfter=3, 
                              textColor=colors.red, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='CustomImprovementItem', fontSize=10, spaceAfter=3, 
                              textColor=colors.green, fontName='Helvetica-Bold'))

    # List to hold all PDF elements
    story = [] 
    
    # 1. Title and Score
    score = data.get('overall_score', 'N/A')
    story.append(Paragraph(f'AI Resume Analysis Report ({score}/100)', styles['CustomHeading1']))
    story.append(Paragraph(f'Reasoning: {data.get("score_reason", "N/A")}', styles['CustomBodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # 2. Suggested Summary
    story.append(Paragraph('Suggested Professional Summary', styles['CustomHeading2']))
    story.append(Paragraph(data.get('summary_rewrite', 'N/A'), styles['CustomBodyText']))
    story.append(Spacer(1, 0.2*inch))

    # 3. ATS Risks
    story.append(Paragraph('🚨 Identified ATS Risks', styles['CustomHeading2']))
    risk_list_items = [
        ListItem(Paragraph(f'{item.get("risk") or item.get("item") or item.get("explanation") or "Generic Risk Title"}: {item["explanation"]}', styles['CustomRiskItem']), bulletText='•') 
        for item in data.get('ats_risks', [])
    ]
    story.append(ListFlowable(risk_list_items, bulletType='bullet', start='bullet', 
                              spaceBefore=5, leftIndent=20))
    story.append(Spacer(1, 0.2*inch))
    
    # 4. ATS Improvements (Assuming the structure is the same as risks)
# 4. ATS Improvements (Assuming the structure is the same as risks)
    story.append(Paragraph('✅ Suggestions for ATS Improvement', styles['CustomHeading2']))
    
    # --- CHANGE IS HERE: Use .get() with the 'risk' OR 'item' key for safety ---
    improvement_list_items = [
        ListItem(
            # Safely check for 'risk', then 'item', and provide a fallback title
            Paragraph(
                f'{item.get("risk") or item.get("item") or item.get("explanation") or "Generic Suggestion"}: {item.get("explanation", "No explanation provided.")}', 
                styles['CustomImprovementItem']
            ), 
            bulletText='•'
        ) 
        for item in data.get('ats_improvements', [])
    ]
    # --------------------------------------------------------------------------

    story.append(ListFlowable(improvement_list_items, bulletType='bullet', start='bullet', 
                              spaceBefore=5, leftIndent=20))
    story.append(Spacer(1, 0.2*inch))
    
    # 5. Detailed Suggestions (Using pre-wrap style for multi-line text)
    story.append(Paragraph('Detailed Suggestions for Overall Improvement', styles['CustomHeading2']))
    
    # Note: ReportLab doesn't natively handle pre-wrap well, simple Paragraph is used
    suggestions = data.get('detailed_suggestions', 'N/A')
    story.append(Paragraph(suggestions.replace('\n', '<br/>'), styles['CustomBodyText']))
    
    # Build the document
    doc.build(story)
    # Move buffer position to the start and return the content
    buffer.seek(0)
    return buffer.read()

# app.py - Corrected download route using ReportLab

@app.route('/report/<report_id>/download')
def download_modified_resume(report_id):
    """
    Generates a PDF report using ReportLab and serves it for download.
    """
    # 1. Retrieve the analysis data
    data = analysis_data_store.get(report_id)
    if not data:
        return jsonify({"error": "Report data not found for PDF generation."}), 404
    
    # 2. GENERATE PDF USING REPORTLAB
    try:
        # Call the new ReportLab helper to get the PDF binary data
        pdf_data = generate_reportlab_pdf(data) 

    except Exception as e:
        print(f"ReportLab PDF generation failed: {e}")
        return jsonify({"error": "PDF creation failed with ReportLab. Check server logs."}), 500
    
    # 3. Serve file to user
    # Note: pdf_data is the final binary output from ReportLab
    return Response(
        pdf_data,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=Gemini_Resume_Report_{report_id}.pdf',
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)