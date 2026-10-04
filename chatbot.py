def generate_chat_response(question, job_role, missing_skills):
    q = question.lower()

    if "skill" in q or "learn" in q:
        if missing_skills:
            return f"For the role of {job_role}, you should focus on learning: {', '.join(missing_skills)}."
        return "Your skills already match the job requirements well."

    if "resume" in q:
        return "Tailor your resume to the job description and highlight relevant projects."

    if "interview" in q:
        return "Revise core concepts, practice problem-solving, and prepare explanations for your projects."

    return "I can help with resume analysis, skill gaps, and interview preparation."
