import cv2
import fitz
import numpy as np
from PIL import Image
import os

drawing = False
start_point = (-1, -1)
end_point = (-1, -1)
boxes = []

def render_page(pdf_path, page_num, zoom=2):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return np.array(img)

def draw_rectangle(event, x, y, flags, param):
    global drawing, start_point, end_point, boxes, temp_img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = temp_img.copy()
            cv2.rectangle(img_copy, start_point, (x, y), (0, 255, 0), 2)
            cv2.imshow("Crop Editor", img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        boxes.append((start_point, end_point))
        cv2.rectangle(temp_img, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Crop Editor", temp_img)

def crop_and_label_service(pdf_path, output_dir):
    global temp_img, boxes
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        print(f"\n--- Page {page_num+1} ---")
        boxes = []
        img = render_page(pdf_path, page_num)
        temp_img = img.copy()

        cv2.namedWindow("Crop Editor", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Crop Editor", draw_rectangle)

        while True:
            cv2.imshow("Crop Editor", temp_img)
            key = cv2.waitKey(0)

            if key == ord('q'):
                break

            elif key == 13:  # Enter = Save crops
                os.makedirs(output_dir, exist_ok=True)
                count = 0
                for (pt1, pt2) in boxes:
                    x1, y1 = pt1
                    x2, y2 = pt2
                    x1, x2 = sorted([x1, x2])
                    y1, y2 = sorted([y1, y2])
                    cropped = img[y1:y2, x1:x2]

                    # Show labeling prompt
                    print(f"\nLabel for crop #{count+1}:")
                    labels = ['diagrams', 'tables', 'equations', 'others']
                    for i, label in enumerate(labels, 1):
                        print(f"{i}. {label}")
                    try:
                        choice = int(input("Enter label number (1–4): "))
                        folder = labels[choice - 1] if 1 <= choice <= 4 else "others"
                    except:
                        folder = "others"

                    folder_path = os.path.join(output_dir, folder)
                    os.makedirs(folder_path, exist_ok=True)
                    file_path = os.path.join(folder_path, f"page_{page_num+1}_{folder}_{count+1}.png")
                    Image.fromarray(cropped).save(file_path)
                    print(f"Saved to {file_path}")
                    count += 1
                break

            elif key == 8:  # Backspace to undo
                if boxes:
                    boxes.pop()
                    temp_img = img.copy()
                    for pt1, pt2 in boxes:
                        cv2.rectangle(temp_img, pt1, pt2, (0, 255, 0), 2)
                    cv2.imshow("Crop Editor", temp_img)

        cv2.destroyAllWindows()
    return "Cropping completed"

