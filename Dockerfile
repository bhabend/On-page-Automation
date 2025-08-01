FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Set environment variable so playwright installs browser in a permanent path
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install ONLY Chromium and ensure it's in the correct path
RUN playwright install chromium

# Expose Streamlit port
EXPOSE 10000

CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
