import os
from PIL import Image
from pix2tex.cli import LatexOCR

def initialize_latex_ocr():
    try:
        model = LatexOCR()
        return model
    except Exception as e:
        return None

def process_single_image(image_path, ocr_model):
    try:
        pil_image = Image.open(image_path)
        latex_code = ocr_model(pil_image)
        if latex_code and latex_code.strip():
            base_name = os.path.splitext(image_path)[0]
            latex_filename = f"{base_name}_latex.txt"
            with open(latex_filename, 'w', encoding='utf-8') as f:
                f.write(f"% LaTeX OCR result for {os.path.basename(image_path)}\n")
                f.write(f"% Generated using pix2tex\n\n")
                f.write(latex_code)
            return True
        return False
    except Exception:
        return False

def batch_latex_ocr(directory_path):
    if not os.path.exists(directory_path):
        return {"error": "Directory not found"}

    ocr_model = initialize_latex_ocr()
    if not ocr_model:
        return {"error": "Failed to initialize OCR model"}

    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
    image_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path)
                   if any(file.lower().endswith(ext) for ext in image_extensions)]

    if not image_files:
        return {"message": "No image files found"}

    summary = {"total": len(image_files), "success": 0, "failed": 0}
    for image in image_files:
        if process_single_image(image, ocr_model):
            summary["success"] += 1
        else:
            summary["failed"] += 1
    return summary
