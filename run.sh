#!/bin/sh

# Define folder paths
DATA_FOLDER="/app/data"
EXCEL_FOLDER="/app/excel_files"
OUTPUT_FOLDER="/app/output"

# Use the GITHUB_SYNC_REPOSITORY environment variable for cloning
git clone $GITHUB_SYNC_REPOSITORY $OUTPUT_FOLDER

# Infinite loop to run the tasks every 10 minutes
while true; do
    echo "Starting download and processing tasks..."
    
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
