from .image_preprocess import preprocess_image
import pytesseract


def ocr_extract_text(image_path, threshold=150):
    try:
        preprocessed_image = preprocess_image(
            image_path, threshold
        )  # preprocess the image

        text = pytesseract.image_to_string(preprocessed_image)  # OCR extraction

        text = text.strip()  # Clean text
        
        print(f"OCR Extracted Text: {text}")  # Debug print
        if not text:
            return "OCR Failed: No text detected"

        return text
    except Exception as e:
        return f"OCR failed: {str(e)}"
