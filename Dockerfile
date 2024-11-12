# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install Git, Cron, rsyslog, and procps (for ps command)
RUN apt-get update && apt-get install -y git cron rsyslog procps && apt-get clean

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

# Ensure the cron job file has proper permissions
RUN chmod 0644 /etc/cron.d/scheduled-task

# Apply the cron job
RUN crontab /etc/cron.d/scheduled-task

# Create the cron log file and set the correct permissions
RUN touch /var/log/cron.log && chmod 0644 /var/log/cron.log

# Configure rsyslog to log cron output to /var/log/cron.log
RUN echo "cron.* /var/log/cron.log" >> /etc/rsyslog.d/50-default.conf

# Start rsyslog and cron daemon in the background when the container runs
CMD cron && rsyslogd && tail -f /var/log/cron.log
