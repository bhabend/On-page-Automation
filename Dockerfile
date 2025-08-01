# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Make sure .env is included
ENV PYTHONUNBUFFERED=1

# Expose the port Streamlit uses
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py"]
