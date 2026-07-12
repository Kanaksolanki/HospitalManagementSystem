"""
Extracts plain text from an uploaded medical report file, so
report_summarizer.py has something to run its regex + AI narrative over
without the patient needing to retype it by hand.

Handles two kinds of input:
  1. Text-based PDFs (e.g. a lab exported a real PDF) -- text is pulled
     directly from the PDF's text layer via PyMuPDF. Fast, no OCR needed.
  2. Scanned/photographed reports (a phone photo of a printed report, or a
     PDF made by "print to PDF" from a camera app, or a plain image file)
     -- these have no real text layer, so each page is rendered to an image
     and run through Tesseract OCR instead.

For PDFs we always try the fast text-layer path first, and only fall back
to OCR per-page if that page's extracted text looks too short to be real
report content (e.g. a scanned page with no text layer returns "" or a
couple of stray characters from a watermark).

Requires the system `tesseract-ocr` package to be installed (not just the
`pytesseract` Python wrapper) -- see README for setup.
"""

import io

import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageOps

# Below this many characters, we treat a PDF page's embedded text as "not
# real content" (e.g. just a stray header/footer) and OCR that page instead.
MIN_TEXT_LAYER_CHARS = 20

# Render scanned PDF pages at this zoom factor before OCR -- higher improves
# accuracy on small print but costs more time/memory. 2x roughly matches a
# 150-200 DPI scan, which is a reasonable phone-photo/PDF-scan resolution.
OCR_RENDER_ZOOM = 2.0

# Phone photos are often lower resolution / lower contrast than a proper
# scan. Upscaling small images and normalizing contrast measurably helps
# Tesseract's accuracy on this kind of input.
OCR_MIN_WIDTH_PX = 1600

IMAGE_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif"}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")


def _preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """Grayscale + upscale + contrast-normalize, so a slightly blurry or
    dim phone photo OCRs closer to how a clean scan would."""
    image = image.convert("L")  # grayscale
    if image.width < OCR_MIN_WIDTH_PX:
        scale = OCR_MIN_WIDTH_PX / image.width
        image = image.resize((int(image.width * scale), int(image.height * scale)), Image.LANCZOS)
    image = ImageOps.autocontrast(image)
    return image


def _ocr_image(image: Image.Image) -> str:
    image = _preprocess_for_ocr(image)
    return pytesseract.image_to_string(image)


def _extract_from_pdf_bytes(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    try:
        for page in doc:
            text_layer = page.get_text().strip()
            if len(text_layer) >= MIN_TEXT_LAYER_CHARS:
                pages_text.append(text_layer)
                continue
            # No usable text layer on this page (likely a scanned image) --
            # render it and OCR it instead.
            pix = page.get_pixmap(matrix=fitz.Matrix(OCR_RENDER_ZOOM, OCR_RENDER_ZOOM))
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            pages_text.append(_ocr_image(img))
    finally:
        doc.close()
    return "\n".join(pages_text).strip()


def _extract_from_image_bytes(file_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(file_bytes))
    return _ocr_image(img).strip()


def extract_report_text(file_bytes: bytes, filename: str = "", content_type: str = "") -> dict:
    """
    Returns {"text": str, "method": "pdf_text" | "pdf_ocr" | "image_ocr", "error": str | None}.

    `method` is "pdf_text" only if every page had a usable embedded text
    layer; if any page needed OCR, it's reported as "pdf_ocr" since accuracy
    is lower and a person reviewing results should know that.
    """
    name_lower = (filename or "").lower()
    is_pdf = name_lower.endswith(".pdf") or content_type == "application/pdf"
    is_image = name_lower.endswith(IMAGE_EXTENSIONS) or content_type in IMAGE_CONTENT_TYPES

    try:
        if is_pdf:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            all_text_layer = all(len(p.get_text().strip()) >= MIN_TEXT_LAYER_CHARS for p in doc) if doc.page_count else False
            doc.close()
            text = _extract_from_pdf_bytes(file_bytes)
            method = "pdf_text" if all_text_layer else "pdf_ocr"
            return {"text": text, "method": method, "error": None}
        elif is_image:
            text = _extract_from_image_bytes(file_bytes)
            return {"text": text, "method": "image_ocr", "error": None}
        else:
            return {"text": "", "method": None, "error": f"Unsupported file type for OCR: {filename}"}
    except Exception as exc:  # noqa: BLE001 -- surface any OCR failure as a clean message, don't crash the upload
        return {"text": "", "method": None, "error": f"Could not read file: {exc}"}