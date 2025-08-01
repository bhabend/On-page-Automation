FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium only and set proper path
RUN playwright install chromium

# Set environment variable to point to installed browsers
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

EXPOSE 10000

CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
