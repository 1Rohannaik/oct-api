from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
import pytesseract

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    try:
        images = convert_from_bytes(pdf_bytes)
    except Exception as e:
        return {"success": False, "error": f"PDF to image conversion failed: {str(e)}"}

    text = ""
    for i, image in enumerate(images):
        try:
            text += pytesseract.image_to_string(image)
        except Exception as e:
            return {"success": False, "error": f"OCR failed on page {i+1}: {str(e)}"}

    return {"success": True, "text": text.strip()}
