# skill_extractor.py
import re

# Expanded skills database
SKILLS_DB = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust", "swift", "kotlin",
    
    # Web Development
    "html", "css", "react", "angular", "vue", "node.js", "node", "express", "django", "flask", "spring", "laravel",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "oracle", "sqlite", "database",
    
    # Cloud & DevOps
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "jenkins", "git", "ci/cd", "terraform",
    
    # Data Science & ML
    "machine learning", "data science", "deep learning", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn",
    "data analysis", "statistics", "power bi", "tableau",
    
    # Mobile Development
    "android", "ios", "react native", "flutter",
    
    # Testing
    "testing", "unit testing", "test automation", "selenium", "jest", "pytest",
    
    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving", "project management", "agile", "scrum"
]

def extract_skills(text):
    """
    Extract skills from text using pattern matching
    """
    if not text:
        return []
    
    text = text.lower()
    skills_found = []
    
    # Check for each skill
    for skill in SKILLS_DB:
        # Create regex pattern to match whole word
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            # Capitalize properly
            if '/' in skill:
                # Handle cases like "HTML/CSS"
                parts = skill.split('/')
                capitalized = '/'.join([p.capitalize() for p in parts])
            else:
                capitalized = skill.title()
            skills_found.append(capitalized)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in skills_found:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    
    return unique_skills[:20]  # Return top 20 skills max