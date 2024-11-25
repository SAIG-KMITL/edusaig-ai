# Use Python 3.11-alpine as base image
FROM python:3.10-slim

# Set environment variables
ARG SAIG_LLM_URL
ENV SAIG_LLM_URL=$SAIG_LLM_URL

ARG SAIG_LLM_MODEL
ENV SAIG_LLM_MODEL=$SAIG_LLM_MODEL

ARG HUGGING_FACE_API_KEY
ENV HUGGING_FACE_API_KEY=$HUGGING_FACE_API_KEY

ARG HUGGING_FACE_ASR_MODEL
ENV HUGGING_FACE_ASR_MODEL=$HUGGING_FACE_ASR_MODEL

# Install system dependencies
RUN apt update && apt install -y \
    gcc \
    g++ \
    musl-dev \
    ffmpeg \
    libffi-dev \
    wine \
    bash \
    curl \
    make \
    && pip install --upgrade pip

# Create and set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code and .env file
COPY . .
COPY .env .

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "./main.py"]
