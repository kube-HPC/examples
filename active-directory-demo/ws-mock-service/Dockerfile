# Use a lightweight Python base
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY ws-service.py .

# Expose port (matches default in ws-service.py)
EXPOSE 5000

# HKube calls start(), so we just launch the script
CMD ["python", "ws-service.py"]
