FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wget gnupg unzip libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpangocairo-1.0-0 libxshmfence1
RUN playwright install

ENV STREAMLIT_PORT=8501
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
