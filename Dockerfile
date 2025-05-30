# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl ca-certificates
RUN update-ca-certificates