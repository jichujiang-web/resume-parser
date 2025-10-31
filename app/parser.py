# app/parser.py
"""
Module to parse resumes (PDF or DOCX) using LLaMA model.
Extracts contact info, experience, skills, and education.
"""

from .utils import extract_text_from_pdf, extract_text_from_docx, clean_model_output
from llama_cpp import Llama
import json
import re

# Load LLaMA model
MODEL_PATH = "models/Llama-3.2-1B-Instruct-f16.gguf"
llama_model = Llama(
    model_path=MODEL_PATH,
    n_ctx=8192,  # Adjust if system can handle more
    n_threads=8,
)


def parse_resume(file_path: str) -> str:
    """
    Parse a resume file (PDF or DOCX) and extract structured information
    using the LLaMA model.

    Args:
        file_path (str): Path to the resume file.

    Returns:
        str: Extracted information as a valid JSON string.
    """
    # Extract raw text based on file type
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

    # Clean the extracted text
    cleaned_text = clean_model_output(raw_text)

    # Build the prompt
    prompt = f"""
Your job is to extract structured resume information from the given text.

You must find and return:
- Contact: full name, email, phone number, location, LinkedIn (if available)
- Experience: company, title, start date, end date, location, description
- Skills: list of relevant skills, languages, tools, or frameworks
- Education: institution, degree, start date, end date, location

Input example:
Tasiana Ukura
tukura@email.com (123) 456-7890 Seattle, WA LinkedIn
WORK EXPERIENCE
Fast - Senior Software Engineer
October 2016 - current Seattle, WA
· Built and maintained application that scaled to 2M daily users, communicating with cross-functional teams regarding product and design
...

------------------
Desired JSON output:
------------------
{{
  "success": true,
  "data": {{
    "contact": {{
      "name": "Tasiana Ukura",
      "email": "tukura@email.com",
      "phone": "(123) 456-7890",
      "location": "Seattle, WA",
      "linkedin": "LinkedIn"
    }},
    "experience": [
      {{
        "company": "Fast",
        "title": "Senior Software Engineer",
        "start_date": "October 2016",
        "end_date": "Current",
        "location": "Seattle, WA",
        "description": "Built and maintained an application that scaled to 2M daily users; collaborated with cross-functional teams; transformed UIs using React to reduce debugging time by 62% and increase views by 31%; mentored 6 interns; led a team improving e-commerce payment protection by 15%."
      }}
      # other experiences ...
    ],
    "skills": [
      "Python", "JavaScript", "C++", "Java", "Django", "NodeJS", "React", "jQuery", "Unix", "Git", "Selenium", "SQL", "NoSQL", "AWS"
    ],
    "education": [
      {{
        "institution": "University of Washington",
        "degree": "B.S. in Computer Science",
        "start_date": "August 2004",
        "end_date": "May 2008",
        "location": "Seattle, WA"
      }}
    ]
  }}
}}

Now, use the same logic to extract information from the following text:

{cleaned_text}

Your output should be a JSON object.
"""

    # Generate model response
    response = llama_model.create_completion(
        max_tokens=3096,
        prompt=prompt,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
    )

    model_output = response['choices'][0]['text'].strip()

    return model_output
