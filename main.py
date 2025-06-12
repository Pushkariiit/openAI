from fastapi import FastAPI
from routers import crop_router, ocr_router

app = FastAPI(title="PDF Crop & LaTeX OCR API")

app.include_router(crop_router.router, prefix="/crop", tags=["Crop"])
app.include_router(ocr_router.router, prefix="/ocr", tags=["OCR"])
