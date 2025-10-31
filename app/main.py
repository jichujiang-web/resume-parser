from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from .parser import parse_resume
import shutil
import os

app = FastAPI(title="Resume Parser API", version="1.0")

# Directory to store uploaded files temporarily
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/parse", response_class=JSONResponse, status_code=200)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to parse a resume file (.pdf or .docx).
    Returns structured JSON containing contact info, experience, skills, and education.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Only allow PDF and DOCX files
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(
            status_code=415,  # Unsupported Media Type
            detail="File format not supported. Upload a .pdf or .docx file."
        )

    try:
        # Save uploaded file temporarily
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Parse the resume
        result = parse_resume(file_path)

        return {"success": True, "data": result}

    except ValueError as ve:
        # For known errors like unsupported file formats
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # Catch all other errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
