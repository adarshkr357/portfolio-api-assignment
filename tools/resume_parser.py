import re
from docx import Document
from PyPDF2 import PdfReader

def parse_resume(filepath):
    ext = filepath.split('.')[-1].lower()
    
    if ext == 'pdf':
        text = extract_text_from_pdf(filepath)
    elif ext in ['doc', 'docx']:
        text = extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file format")
    
    return generate_portfolio_data(text)

def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(path):
    text = ""
    doc = Document(path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def generate_portfolio_data(text):
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_section(text, ['skills', 'technical'], max_lines=5)
    experience = extract_section(text, ['experience', 'work'], max_lines=5)
    education = extract_section(text, ['education', 'academic'], max_lines=3)
    about = extract_section(text, ['about', 'summary', 'objective'], max_lines=4)

    return {
        "hero": {
            "name": name,
            "bio": about or "Passionate individual looking to make a difference."
        },
        "about": {
            "description": "\n".join(about) if about else "About section not available."
        },
        "skills": skills or ["Python", "Teamwork", "Problem Solving"],
        "experience": experience or ["Intern at XYZ Corp", "Freelance Developer"],
        "education": education or ["B.Sc in Computer Science"],
        "contact": {
            "email": email,
            "phone": phone
        }
    }

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        if len(line.strip()) > 2 and len(line.strip().split()) <= 4:
            return line.strip()
    return "Unknown Name"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-\(\)]{7,}', text)
    return match.group(0) if match else "Not found"

def extract_section(text, keywords, max_lines=5):
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword in line.lower():
                return [l.strip() for l in lines[i+1:i+1+max_lines] if l.strip()]
    
    return []
