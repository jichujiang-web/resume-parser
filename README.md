# Resume Parser API

## Project Description
This project provides a simple API to parse resumes in **PDF** or **DOCX** format and extract structured information such as **contact details, work experience, skills, and education**. It uses a local **LLaMA model** for text understanding and **FastAPI** for serving the API.

---

## Project Structure

```mermaid
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


Tech Stack

Python 3.11+

FastAPI – Web framework for building the API

Uvicorn – ASGI server

pdfplumber – PDF text extraction

python-docx – DOCX text extraction

LLaMA (llama-cpp-python) – Local language model for parsing

Docker – Containerization for easy setup

Setup / Installation

You can set up the API in two ways:

Option 1: Using the pre-built Docker container

Clone the repository:
