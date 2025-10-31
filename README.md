# Resume Parser API

## Project Description
This project provides a simple API to parse resumes in **PDF** or **DOCX** format and extract structured information such as **contact details, work experience, skills, and education**. It uses a local **LLaMA model** for text understanding and **FastAPI** for serving the API.

---
Project Sturcture :

flowchart TD
    A[User uploads resume] --> B[FastAPI Endpoint /api/parse]
    B --> C[Save file to uploads/]
    C --> D[Parser Module]
    D -->|PDF| E[Extract text with pdfplumber]
    D -->|DOCX| F[Extract text with python-docx]
    E --> G[Clean extracted text]
    F --> G
    G --> H[LLaMA Model: Extract structured JSON]
    H --> I[Post-process & parse JSON]
    I --> J[Return API Response]
    J --> K[User receives structured resume data]

    
    style A fill:#f9f,stroke:#333,stroke-width:1px
    style B fill:#bbf,stroke:#333,stroke-width:1px
    style I fill:#ffb,stroke:#333,stroke-width:1px


resume-parser/
│
├─ app/
│  ├─ main.py           # FastAPI entrypoint
│  ├─ parser.py         # Resume parsing logic
│  └─ utils.py          # Helper functions for PDF/DOCX extraction & cleaning
│
├─ models/              # Folder to store LLaMA model
├─ uploads/             # Temporary upload folder
├─ Dockerfile
├─ requirements.txt
└─ README.md

## Tech Stack
- **Python 3.11+**
- **FastAPI** – Web framework for building the API
- **Uvicorn** – ASGI server
- **pdfplumber** – PDF text extraction
- **python-docx** – DOCX text extraction
- **LLaMA (llama-cpp-python)** – Local language model for parsing
- **Docker** – Containerization for easy setup

---

## Setup / Installation

### **Option 1: Using Docker (Recommended)**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-parser.git
   cd resume-parser


2. Build the docker image
docker load -i resume-parser.tar

3. Run the container:
docker run -d -p 8000:8000 resume-parser:latest

4. API is now available at: http://localhost:8000/docs, you can deploy it at any port of your chocie but make sure to add "/docs" at the end to get access to swagger UI


example output:

using the senior software engineer resume, we can get json output such as this: 

{
  "success": true,
  "data": "{\n  \"success\": true,\n  \"data\": {\n    \"contact\": {\n      \"name\": \"CYNTHIA DWAYNE\",\n      \"email\": \"cynthia@beamjobs.com\",\n      \"phone\": \"(123) 456-7890\",\n      \"location\": \"New York, NY\"\n    },\n    \"experience\": [\n      {\n        \"company\": \"QuickBooks\",\n        \"title\": \"Software Developer\",\n        \"start_date\": \"January 2017\",\n        \"end_date\": \"Current\",\n        \"location\": \"Brooklyn, NY\",\n        \"description\": \"Worked on the payments team; migrated to AWS and reduced cloud costs by $260,000 per year.\"\n      },\n      {\n        \"company\": \"Front-End Developer\",\n        \"title\": \"Front-End Developer\",\n        \"start_date\": \"January 2014\",\n        \"end_date\": \"December 2016\",\n        \"location\": \"New York, NY\",\n        \"description\": \"Contributed to UI library; created reusable components; improved customer conversion rate by 17%.\"\n      }\n    ],\n    \"skills\": [\n      \"Python\", \"JavaScript\", \"Cloud (GCP, AWS)\", \"SQL (PostgreSQL, MySQL)\", \"TypeScript\"\n    ],\n    \"education\": [\n      {\n        \"institution\": \"University of Delaware\",\n        \"degree\": \"Bachelor of Science in Computer Science\",\n        \"start_date\": \"August 2008\",\n        \"end_date\": \"May 2012\",\n        \"location\": \"Newark, DE\"\n      }\n    ]\n  }\n}\n\n------------------\n\nThis is a bit more complex because the text contains multiple job descriptions and skills. Here's my attempt to extract structured resume information from this text:\n\n```json\n{\n  \"success\": true,\n  \"data\": {\n    \"contact\": {\n      \"name\": \"CYNTHIA DWAYNE\",\n      \"email\": \"cynthia@beamjobs.com\",\n      \"phone\": \"(123) 456-7890\",\n      \"location\": \"New York, NY\"\n    },\n    \"experience\": [\n      {\n        \"company\": \"QuickBooks\",\n        \"title\": \"Software Developer\",\n        \"start_date\": \"January 2017\",\n        \"end_date\": \"Current\",\n        \"description\": \"Worked on the payments team; migrated to AWS and reduced cloud costs by $260,000 per year.\",\n        \"skills\": [\n          \"Python\", \"JavaScript\"\n        ],\n        \"education\": [\n          {\n            \"institution\": \"University of Delaware\",\n            \"degree\": \"Bachelor of Science in Computer Science\",\n            \"start_date\": \"August 2008\",\n            \"end_date\": \"May 2012\",\n            \"location\": \"Newark, DE\"\n          }\n        ]\n      },\n      {\n        \"company\": \"Front-End Developer\",\n        \"title\": \"Front-End Developer\",\n        \"start_date\": \"January 2014\",\n        \"end_date\": \"December 2016\",\n        \"description\": \"Contributed to UI library; created reusable components; improved customer conversion rate by 17%.\",\n        \"skills\": [\n          \"Python\", \"JavaScript\", \"Cloud (GCP, AWS)\"\n        ],\n        \"education\": [\n          {\n            \"institution\": \"University of Delaware\",\n            \"degree\": \"Bachelor of Science in Computer Science\",\n            \"start_date\": \"August 2008\",\n            \"end_date\": \"May 2012\",\n            \"location\": \"Newark, DE\"\n          }\n        ]\n      }\n    ],\n    \"skills\": [\n      \"Python\", \"JavaScript\", \"Cloud (GCP, AWS)\", \"SQL (PostgreSQL, MySQL)\", \"TypeScript\"\n    ],\n    \"education\": [\n      {\n        \"institution\": \"University of Delaware\",\n        \"degree\": \"Bachelor of Science in Computer Science\",\n        \"start_date\": \"August 2008\",\n        \"end_date\": \"May 2012\",\n        \"location\": \"Newark, DE\"\n      }\n    ]\n  }\n}\n```\n\nThis output contains the following information:\n\n- Contact details: full name, email, phone number\n- Experience:\n  - Job title and company (with start and end dates)\n  - Description of job responsibilities\n  - Skills used in the job\n- Education:\n  - Institution\n  - Degree earned\n  - Start date\n  - End date\n  - Location\n\nLet me know if this is correct or if you need any further assistance!"
}

## Design Decisions & Considerations

### **Library and Approach Choices**
- **FastAPI**: Chosen for its simplicity, automatic OpenAPI docs, and async support for handling uploads efficiently.
- **pdfplumber & python-docx**: Lightweight and reliable libraries for extracting text from PDF and DOCX files without requiring heavy dependencies like LibreOffice.
- **llama-cpp-python**: Enables local LLaMA inference without relying on cloud APIs, providing more control over data privacy.

### **Accuracy / Reliability Tradeoffs**
- Regex-based extraction is fast but can miss unusual formats of emails or phone numbers.
- LLaMA model extraction is context-based but may produce incomplete or inconsistent JSON when resumes exceed the context window.
- To handle large resumes, text is **chunked**, which may occasionally split information across chunks. JSON merging attempts to mitigate this but may require post-processing for perfect accuracy.

### **Future Improvements**
- **Better entity extraction**: Use NLP libraries or fine-tune LLaMA to reliably extract names, roles, and organizations.
- **Chunk merging logic**: Implement smarter merging of chunked JSON results to avoid duplicates or partial records.
- **Validation & error checking**: Add schema validation (e.g., using `pydantic`) for extracted JSON to ensure consistent output.
- **Complex LLMs**: Integrate with cloud platforms to enable the use of more complex LLMs to improve speed and accuracy.

### **Scaling to Thousands of Resumes/Day**
- Move the LLaMA model to GPU for faster inference or consider batching multiple resumes.  
- Introduce a queue system (e.g., **Celery + Redis**) for asynchronous resume parsing.
- Store results in a database to prevent repeated parsing and allow retrieval at scale.
- Deploy behind a load balancer with multiple instances for horizontal scaling.

### **Additional Features Valuable in Production**
- Resume versioning and audit logs for traceability.
- Multi-language support for resumes in different languages.
- Web interface for drag-and-drop uploads or bulk processing.
- Real-time analytics on parsed resumes (skills, roles, trends).
- Integration with ATS (Applicant Tracking Systems) or HR platforms.

Known Limitations:
-Large resumes may exceed model context window
-model output isnt exactly json structure, can use more post processing or use a better LLM
-LLaMA model requires local GPU for best performance; CPU inference is slower



