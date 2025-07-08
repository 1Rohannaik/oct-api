from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read PDF bytes
        pdf_bytes = await file.read()

        # Convert PDF to images
        try:
            images = convert_from_bytes(pdf_bytes)
        except Exception as conv_err:
            return {
                "success": False,
                "error": f"PDF to image conversion failed: {str(conv_err)}"
            }

        # Run OCR
        text = ""
        for i, image in enumerate(images):
            try:
                text += pytesseract.image_to_string(image)
            except Exception as ocr_err:
                return {
                    "success": False,
                    "error": f"OCR failed on page {i+1}: {str(ocr_err)}"
                }

        if not text.strip():
            return {
                "success": False,
                "error": "OCR returned empty text."
            }

        return {
            "success": True,
            "text": text.strip()
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
