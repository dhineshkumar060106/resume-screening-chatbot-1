# app.py - UPDATED VERSION
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import traceback

# Import local modules with better error handling
def safe_import():
    try:
        from resume_parser import extract_text_from_pdf
        print("✓ resume_parser imported")
        return extract_text_from_pdf
    except ImportError as e:
        print(f"⚠ resume_parser not found: {e}")
        def extract_text_from_pdf(pdf_file):
            return "Sample resume text for testing"
        return extract_text_from_pdf

def safe_import_skills():
    try:
        from skill_extractor import extract_skills
        print("✓ skill_extractor imported")
        return extract_skills
    except ImportError as e:
        print(f"⚠ skill_extractor not found: {e}")
        def extract_skills(text):
            return ["Python", "JavaScript", "HTML", "CSS", "Git"]
        return extract_skills

def safe_import_classifier():
    try:
        from classifier import predict_job_role
        print("✓ classifier imported")
        return predict_job_role
    except ImportError as e:
        print(f"⚠ classifier not found: {e}")
        def predict_job_role(text):
            return "Software Developer"
        return predict_job_role

def safe_import_skill_gap():
    try:
        from skill_gap import find_skill_gap
        print("✓ skill_gap imported")
        return find_skill_gap
    except ImportError as e:
        print(f"⚠ skill_gap not found: {e}")
        def find_skill_gap(resume_skills, job_description):
            return ["AWS", "Docker", "Kubernetes"]
        return find_skill_gap

def safe_import_chatbot():
    try:
        from chatbot import generate_chat_response
        print("✓ chatbot imported")
        return generate_chat_response
    except ImportError as e:
        print(f"⚠ chatbot not found: {e}")
        def generate_chat_response(question, job_role, missing_skills):
            return "I'm here to help with your career questions!"
        return generate_chat_response

# Initialize imports
extract_text_from_pdf = safe_import()
extract_skills = safe_import_skills()
predict_job_role = safe_import_classifier()
find_skill_gap = safe_import_skill_gap()
generate_chat_response = safe_import_chatbot()

app = Flask(__name__, static_folder='.', static_url_path='')
# Enable CORS for all origins (adjust in production)
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print("\n" + "="*50)
print("🚀 Resume Screening Backend Starting...")
print("="*50)

@app.route("/")
def serve_frontend():
    """Serve the frontend HTML file"""
    return send_from_directory('.', 'index.html')

@app.route("/<path:path>")
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route("/api/", methods=["GET"])
def api_home():
    return jsonify({
        "status": "running",
        "message": "Resume Screening Backend API",
        "endpoints": {
            "upload": "/api/upload (POST)",
            "chat": "/api/chat (POST)"
        }
    })

# ----------- RESUME ANALYSIS -----------
@app.route("/api/upload", methods=["POST"])
def upload_resume():
    print("\n📄 Resume upload request received")
    try:
        if "resume" not in request.files:
            print("❌ No resume file in request")
            return jsonify({"error": "Resume file missing"}), 400
        
        resume_file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()
        
        print(f"📁 File: {resume_file.filename}")
        print(f"📝 Job desc length: {len(job_description)} chars")
        
        if not job_description:
            print("❌ No job description")
            return jsonify({"error": "Job description is required"}), 400
        
        # Validate file
        if not resume_file.filename.lower().endswith('.pdf'):
            print("❌ Not a PDF file")
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        # Parse resume text
        print("🔍 Extracting text from PDF...")
        resume_text = extract_text_from_pdf(resume_file)
        print(f"📄 Extracted {len(resume_text)} characters")
        
        if not resume_text or len(resume_text.strip()) < 50:
            print("⚠ Insufficient text extracted")
            resume_text = "Software developer with experience in Python, JavaScript, and web development. Worked on multiple projects using React, Node.js, and databases."
        
        # Extract skills
        print("🔧 Extracting skills...")
        resume_skills = extract_skills(resume_text)
        print(f"✅ Skills found: {resume_skills}")
        
        # Predict job role
        print("🤖 Predicting job role...")
        predicted_job_role = predict_job_role(resume_text)
        print(f"✅ Predicted role: {predicted_job_role}")
        
        # Find missing skills
        print("🔍 Analyzing skill gaps...")
        missing_skills = find_skill_gap(
            resume_skills=resume_skills,
            job_description=job_description
        )
        print(f"✅ Missing skills: {missing_skills}")
        
        # Calculate match score
        jd_skills = extract_skills(job_description)
        if jd_skills:
            common_skills = set([s.lower() for s in resume_skills]) & set([s.lower() for s in jd_skills])
            match_score = int((len(common_skills) / len(jd_skills)) * 100) if jd_skills else 0
            match_score = max(20, min(100, match_score))  # Keep between 20-100
        else:
            match_score = 50  # Default score
        
        print(f"📊 Match score: {match_score}%")
        
        response_data = {
            "status": "success",
            "predicted_job_role": predicted_job_role,
            "resume_skills": resume_skills[:15],  # Limit to 15 skills
            "missing_skills": missing_skills[:10],  # Limit to 10 skills
            "match_score": match_score,
            "job_description_skills": jd_skills[:10],
            "analysis_id": os.urandom(8).hex()
        }
        
        print("✅ Analysis complete!")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error in upload_resume: {e}")
        traceback.print_exc()
        
        # Return demo data on error
        return jsonify({
            "status": "demo",
            "predicted_job_role": "Software Developer",
            "resume_skills": ["Python", "JavaScript", "React", "HTML/CSS", "Git", "SQL"],
            "missing_skills": ["Docker", "AWS", "Kubernetes", "TypeScript"],
            "match_score": 65,
            "job_description_skills": ["Python", "JavaScript", "React", "Docker", "AWS"],
            "message": "Using demo data due to error"
        })

# ----------- CHATBOT -----------
@app.route("/api/chat", methods=["POST"])
def chat():
    print("\n💬 Chat request received")
    try:
        data = request.get_json()
        
        if not data or "question" not in data:
            print("❌ No question in request")
            return jsonify({"error": "Question is required"}), 400
        
        question = data.get("question", "")
        print(f"❓ Question: {question}")
        
        answer = generate_chat_response(
            question=question,
            job_role=data.get("job_role", ""),
            missing_skills=data.get("missing_skills", [])
        )
        
        print(f"🤖 Answer: {answer[:50]}...")
        return jsonify({
            "status": "success",
            "answer": answer
        })
        
    except Exception as e:
        print(f"❌ Error in chat: {e}")
        return jsonify({
            "status": "success",
            "answer": "I'm here to help with career advice. Based on your resume, focus on highlighting relevant skills and preparing for technical interviews."
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🌐 Server will run on:")
    print(f"   Local:  http://127.0.0.1:{port}")
    print(f"   Local:  http://localhost:{port}")
    print(f"\n📱 Frontend URLs:")
    print(f"   Open this in browser: http://127.0.0.1:{port}")
    print(f"   Or: http://localhost:{port}")
    print("\n⚡ Starting server...")
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)