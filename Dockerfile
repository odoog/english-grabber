# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts and data folder to the container
COPY download_excel.py .
COPY excel_to_md.py .
COPY git_push.sh .
COPY run.sh .
COPY data /app/data

# Make the scripts executable
RUN chmod +x git_push.sh run.sh

# Create required directories, except the existing 'data' folder
RUN mkdir -p /app/excel_files /app/output

# Use the run.sh script as the container's entrypoint
ENTRYPOINT ["sh", "./run.sh"]
