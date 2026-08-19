# Use an official, lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the image container
COPY requirements.txt .

# Install dependencies without storing cache files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code files
COPY . .

# Expose port 5000 inside the container
EXPOSE 5000

# Specify environment variable configurations
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Define the command to execute your application
CMD ["python", "app.py"]
