# Use the official Playwright Python image
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render (they expect port 10000)
EXPOSE 10000

# Run the Streamlit app on the required port/address
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
