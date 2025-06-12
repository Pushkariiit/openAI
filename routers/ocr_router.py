from fastapi import APIRouter, Form
from services.ocr_service import batch_latex_ocr

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)

@router.post("/batch")
def ocr_batch(directory: str = Form(...)):
    """
    Run LaTeX OCR on all images in a directory.
    Pass `directory` as a form field containing the absolute path.
    Example: directory=C:/Users/DELL/OneDrive/Desktop/AI-Prepzy/your_image_folder
    """
    return batch_latex_ocr(directory)
