FROM python:3.10-slim

# Install Chromium and required packages
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    build-essential \
    libglib2.0-0 libnss3 libgconf-2-4 \
    libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 libgtk-3-0 \
    wget curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable so Playwright uses system Chromium
ENV PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit
EXPOSE 10000

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
