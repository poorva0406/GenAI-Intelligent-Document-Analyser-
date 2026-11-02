FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8501
# Until the Streamlit UI exists (Phase 7), the container runs diagnostics.
# Then switch to: CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0"]
CMD ["python", "run.py", "check"]
