# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 5000 (internal) mapped externally (e.g., 5001)
EXPOSE 5000

# Initialize the DB and run the app using Gunicorn for production (use flask for dev)
CMD ["sh", "-c", "python app/init_db.py && python app/main.py"]
