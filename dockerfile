# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /Main_platform/drf

# Copy the current directory contents into the container at /Main_platform/drf
COPY . /Main_platform/drf

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the /app/media directory for file uploads
RUN mkdir -p /app/media

# Expose the port that Django runs on
EXPOSE 8000
# ... (기존 내용을 유지한 상태에서)
# Copy the Gunicorn configuration file into the container at /app
COPY gunicorn.conf.py /Main_platform/drf/

# Start Gunicorn with the custom configuration
CMD ["gunicorn", "project_name.wsgi:application", "--config", "gunicorn.conf.py"]

