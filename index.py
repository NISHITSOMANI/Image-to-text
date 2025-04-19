from flask import Flask, request, render_template
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pdf2image import convert_from_bytes
import io

app = Flask(__name__)

# Optional: Limit file size (5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Preprocess image for better OCR accuracy
def preprocess_image(image):
    gray = image.convert('L')  # Grayscale
    gray = gray.filter(ImageFilter.SHARPEN)  # Sharpen
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)  # Increase contrast
    return gray

@app.route('/', methods=['GET', 'POST'])
def home():
    text = ""
    if request.method == 'POST':
        uploaded_file = request.files.get('file')

        if not uploaded_file or not uploaded_file.filename:
            text = "⚠️ No file uploaded. Please select a valid image or PDF."
        else:
            try:
                file_bytes = uploaded_file.read()

                if uploaded_file.filename.lower().endswith('.pdf'):
                    # Convert PDF to images
                    pages = convert_from_bytes(file_bytes)
                    for page in pages:
                        preprocessed = preprocess_image(page)
                        text += pytesseract.image_to_string(preprocessed, lang='eng') + '\n'
                else:
                    # Handle image files
                    image = Image.open(io.BytesIO(file_bytes))
                    preprocessed = preprocess_image(image)
                    text = pytesseract.image_to_string(preprocessed, lang='eng')

            except Exception as e:
                text = f"⚠️ Error while processing the file: {str(e)}"

    return render_template('index.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)
