FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and dependencies
RUN apt-get update && apt-get install -y wget gnupg libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 libatspi2.0-0 \
    && pip install playwright \
    && playwright install --with-deps

# Expose the port Streamlit will run on
EXPOSE 10000

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
