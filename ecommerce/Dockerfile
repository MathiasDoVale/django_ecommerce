# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Copy entrypoint script into the image
COPY entrypoint.sh /code/

# Copy wait-for-it script into the image
COPY wait-for-it.sh /code/

# Install dos2unix and convert line endings of the scripts
RUN apt-get update && apt-get install -y dos2unix && dos2unix /code/entrypoint.sh && dos2unix /code/wait-for-it.sh

# Make the script executable
RUN chmod +x /code/wait-for-it.sh

# Make the script executable
RUN chmod +x /code/entrypoint.sh

# Run the entrypoint script when the container starts
ENTRYPOINT ["/code/entrypoint.sh"]