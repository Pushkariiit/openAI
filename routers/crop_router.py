from fastapi import APIRouter, UploadFile, Form
from services.crop_service import crop_and_label_service

router = APIRouter()

@router.post("/extract")
async def extract_and_crop(pdf: UploadFile, output_dir: str = Form(...)):
    """
    Accepts a PDF file and allows cropping using OpenCV GUI.
    """
    pdf_path = f"temp_{pdf.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await pdf.read())

    result = crop_and_label_service(pdf_path, output_dir)
    return {"status": result}
