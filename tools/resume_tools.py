# tools/resume_tools.py
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
from docx import Document
import tempfile
import os
import re

def tailor_resume_from_file(file_path: str, job_description: str, company: str = None, job_title: str = None):
    """
    Takes an uploaded resume file (PDF or DOCX), tailors it to a job description,
    and outputs a rewritten PDF version.
    """
    # ✅ Step 1: Extract text from the uploaded file
    text = ""
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type. Please upload a .pdf or .docx resume.")

    # ✅ Step 2: Rewrite resume with OpenAI
    llm = OpenAI(model="gpt-4o")

    prompt = f"""
    You are a professional resume editor.
    Rewrite the following resume so that it matches the provided job description,
    emphasizing relevant experience, keywords, and formatting.

    === JOB DESCRIPTION ===
    {job_description}

    === ORIGINAL RESUME ===
    {text}

    Please output the improved resume text, formatted as a professional resume.
    """

    rewritten_text = llm.complete(prompt).text.strip()

    # ✅ Step 3: Create a new PDF
    safe_company = re.sub(r"[^a-zA-Z0-9]", "_", company or "Company")
    safe_title = re.sub(r"[^a-zA-Z0-9]", "_", job_title or "Position")
    output_name = f"resume_{safe_company}_{safe_title}.pdf"

    pdf_path = os.path.join(tempfile.gettempdir(), output_name)
    c = canvas.Canvas(pdf_path, pagesize=LETTER)
    width, height = LETTER

    text_obj = c.beginText(50, height - 50)
    text_obj.setFont("Helvetica", 11)

    for line in rewritten_text.split("\n"):
        if not line.strip():
            text_obj.textLine("")
        else:
            text_obj.textLine(line.strip())

        if text_obj.getY() < 50:  # New page if needed
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(50, height - 50)
            text_obj.setFont("Helvetica", 11)

    c.drawText(text_obj)
    c.save()

    return {
        "tailored_resume_text": rewritten_text,
        "pdf_path": pdf_path
    }

tailor_resume_tool = FunctionTool.from_defaults(
    fn=tailor_resume_from_file,
    name="tailor_resume_from_file",
    description="Takes a PDF/DOCX resume file, tailors it to a job description, and outputs a new PDF."
)
