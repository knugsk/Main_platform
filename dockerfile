# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /drf/drf

# Copy the current directory contents into the container at /drf/drf
COPY . /drf/drf/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the /app/media directory for file uploads
RUN mkdir -p /app/media

# Expose the port that Django runs on
EXPOSE 8000

# Run Django with Gunicorn when the container starts
CMD ["python3", "manage.py", "runserver"]
