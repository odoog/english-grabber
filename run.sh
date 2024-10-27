#!/bin/sh

# ---------------------------- Prepare output repository ------------------------------------

# Define folder paths
APP_FOLDER="/app/"
DATA_FOLDER="/app/data"
EXCEL_FOLDER="/app/excel_files"
OUTPUT_FOLDER="/app/output"

if [ ! -d "$OUTPUT_FOLDER" ]; then
    mkdir -p "$OUTPUT_FOLDER"
    echo "Created output directory: $OUTPUT_FOLDER"
fi

cd "$OUTPUT_FOLDER" || exit 1

# Initialize a new Git repository
if [ ! -d ".git" ]; then
    git init
    echo "Initialized a new Git repository in $OUTPUT_FOLDER"
fi

# Check if the remote is already added
if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "$GITHUB_SYNC_REPOSITORY"
    echo "Added remote repository: $GITHUB_SYNC_REPOSITORY"
fi

# ---------------------------- Run endless files update and synchronization ------------------------------------

# Infinite loop to run the tasks every 60 minutes
while true; do
    echo "Starting download and processing tasks..."

    # Update output repository from git
    cd "$OUTPUT_FOLDER" || exit 1
    git pull origin main

    # Work in app folder
    cd "$APP_FOLDER" || exit 1

    # Run the download script
    python download_excel.py $DATA_FOLDER/file_ids.txt $EXCEL_FOLDER
    if [ $? -ne 0 ]; then
        echo "Error running download_excel.py"
        sleep 600
        continue
    fi

    # Run the Excel to MD conversion script, outputting directly to the Git-synced folder
    python excel_to_md.py $EXCEL_FOLDER $OUTPUT_FOLDER
    if [ $? -ne 0 ]; then
        echo "Error running excel_to_md.py"
        sleep 600
        continue
    fi

    # Push to GitHub
    ./git_push.sh
    if [ $? -ne 0 ]; then
        echo "Error running git_push.sh"
    fi

    # Wait 10 minutes before running the tasks again
    echo "Waiting for 60 minutes..."
    sleep 600
done
