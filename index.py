from flask import Flask, render_template, request
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pdf2image import convert_from_bytes
import io
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__, template_folder="templates")

def preprocess_image(image):
    image = image.convert('L')  # Grayscale
    image = image.point(lambda p: p > 200 and 255)
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    image = image.filter(ImageFilter.MedianFilter())
    return image

@app.route("/", methods=["GET", "POST"])
def home():
    extracted_text = ""
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            pages = convert_from_bytes(file.read())
            for page in pages:
                img = preprocess_image(page)
                extracted_text += pytesseract.image_to_string(img) + "\n"
        else:
            img = Image.open(file.stream)
            img = preprocess_image(img)
            extracted_text = pytesseract.image_to_string(img)
    return render_template("index.html", text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
