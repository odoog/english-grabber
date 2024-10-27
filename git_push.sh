#!/bin/sh

# Change to the output directory
cd /app/output/md_files

# Configure Git
git config --global user.name "odoog"
git config --global user.email "odoog@yandex.ru"

# Add all new or modified files
git add .

# Commit changes with a message
git commit -m "Automated update: Processed MD files"

# Push changes to the remote repository
git push origin main
