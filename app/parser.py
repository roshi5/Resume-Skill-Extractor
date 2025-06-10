import re
import pdfplumber

import re
import pdfplumber

def parse_resume(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # Safely extract name
    names = re.findall(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", text)
    name = names[0] if names else "Not Found"

    # Safely extract email
    emails = re.findall(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", text)
    email = emails[0] if emails else "Not Found"

    # Safely extract phone
    phones = re.findall(r"\+?\d[\d\s\-]{8,13}\d", text)
    phone = phones[0] if phones else "Not Found"

    # Extract skills
    skills_match = re.findall(r"(?i)(skills|technologies)[\s:]*([\w\s,]+)", text)
    skills = skills_match[0][1].split(",") if skills_match else []

    # Extract experience block
    experience_match = re.findall(r"(?i)(experience|work history)[\s\S]{0,500}", text)
    experience = experience_match[0] if experience_match else "Not Found"

    return {
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "skills": [s.strip() for s in skills],
        "experience": experience.strip() if isinstance(experience, str) else str(experience)
    }

