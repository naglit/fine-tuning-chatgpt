# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir Flask

# Install additional dependencies if you have them, e.g., from a requirements file
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# If using OpenAI or other specific packages, add their installation here
RUN pip install openai

# Expose port 5000 (Flask's default port)
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
