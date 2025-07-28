
---

###`Dockerfile` (for Round 1B)

```dockerfile
# Dockerfile for Adobe Hackathon Round 1B - Persona-Driven Document Intelligence

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy code and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for PDFs and language detection
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libgl1 \
 && rm -rf /var/lib/apt/lists/*

# Copy rest of the project files
COPY . .

# Entry point
CMD ["python3", "main.py"]

