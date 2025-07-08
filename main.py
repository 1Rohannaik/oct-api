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
        pdf_bytes = await file.read()
        images = convert_from_bytes(pdf_bytes)

        text = ""
        for i, image in enumerate(images):
            text += pytesseract.image_to_string(image)

        return {
            "success": True,
            "text": text.strip()
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

