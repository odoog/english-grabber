# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install Git and Cron
RUN apt-get update && apt-get install -y git cron && apt-get clean

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

# Copy the cron job definition to the container
COPY cronfile /etc/cron.d/scheduled-task

# Give the cron file proper permissions
RUN chmod 0644 /etc/cron.d/scheduled-task

# Apply the cron job
RUN crontab /etc/cron.d/scheduled-task

# Start cron and run.sh
CMD cron && tail -f /var/log/cron.log
