# skill_gap.py
from skill_extractor import extract_skills

def find_skill_gap(resume_skills, job_description):
    """
    Find skills mentioned in job description but missing from resume
    """
    if not job_description:
        return []
    
    # Extract skills from job description
    jd_skills = extract_skills(job_description)
    
    # Convert resume skills to lowercase for comparison
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    # Find missing skills
    missing = []
    for skill in jd_skills:
        skill_lower = skill.lower()
        if skill_lower not in resume_skills_lower:
            missing.append(skill)
    
    return missing[:10]  # Return top 10 missing skills max