FROM python:3.10-slim

WORKDIR /app

# Install test tool (no runtime dependencies required for the app itself)
RUN pip install --no-cache-dir pytest

# Copy application files
COPY . /app

# Default to showing help when container runs without args
CMD ["python", "book_app.py", "help"]
