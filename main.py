from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import logging
import io

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def health_check():
    return {"message": "OCR API is running"}

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}")
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)
        logger.info(f"Extracted text: {text[:100]}...")  # Log first 100 characters
        return {"extracted_text": text}
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Failed to extract text"})
