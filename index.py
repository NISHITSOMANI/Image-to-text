import os
from flask import Flask, request, render_template
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pdf2image import convert_from_bytes
import io

app = Flask(__name__)

def preprocess_image(image):
    # Convert to grayscale
    gray = image.convert('L')
    # Sharpen and increase contrast
    gray = gray.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2)
    # Optional: Binarize (thresholding)
    return gray

@app.route('/', methods=['GET', 'POST'])
def home():
    text = ""
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            file_bytes = uploaded_file.read()

            if uploaded_file.filename.endswith('.pdf'):
                pages = convert_from_bytes(file_bytes)
                for page in pages:
                    pre_img = preprocess_image(page)
                    text += pytesseract.image_to_string(pre_img, lang='eng') + '\n'
            else:
                image = Image.open(io.BytesIO(file_bytes))
                pre_img = preprocess_image(image)
                text = pytesseract.image_to_string(pre_img, lang='eng')

    return render_template('index.html', text=text)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
