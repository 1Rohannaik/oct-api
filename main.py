from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)


@app.get("/")
def health_check():
    return {"message": "OCR API is running "}


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()

        # Convert PDF to images
        images = convert_from_bytes(pdf_bytes)
        logging.info(f"Converted PDF to {len(images)} page(s)")

        text = ""
        for i, image in enumerate(images):
            ocr_text = pytesseract.image_to_string(image)
            logging.info(f"Page {i + 1} OCR length: {len(ocr_text)}")
            text += ocr_text

        if not text.strip():
            raise ValueError("No text extracted from PDF.")

        return {
            "success": True,
            "text": text.strip()
        }

    except Exception as e:
        logging.error(f"OCR extraction failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }
