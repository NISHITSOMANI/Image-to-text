FROM python:3.9-slim

# Install tesseract and poppler for PDF support
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils libglib2.0-0 libsm6 libxext6 libxrender1 && \
    apt-get clean

# Set environment variable for pytesseract to find tesseract binary
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata"

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use gunicorn to serve the app
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app.index:app"]
