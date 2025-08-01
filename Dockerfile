# Use Playwright's official image
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Set working directory
WORKDIR /app

# Copy your app into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (especially Chromium)
RUN playwright install chromium

# Expose required port for Streamlit on Render
EXPOSE 10000

# Start your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
