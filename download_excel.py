import requests
import os
import argparse
import time

def download_excel_files(input_file, output_directory, retries=3, delay=5):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Read file IDs and names from the input text file
    with open(input_file, 'r') as f:
        file_entries = [line.strip().split('_') for line in f if line.strip()]
    
    # Loop over each entry and download the Excel file
    for entry in file_entries:
        if len(entry) < 2:
            print(f"Invalid entry: {entry}. Skipping.")
            continue
        
        file_id, file_name = entry[0], entry[1]
        url = f"https://dictionary.cambridge.org/plus/wordlist/{file_id}/export"
        attempt = 0
        
        while attempt < retries:
            try:
                print(f"Downloading from {url} (Attempt {attempt + 1})...")

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

                response = requests.get(url, headers=headers, timeout=10)
                
                # Check if the download was successful
                if response.status_code == 200:
                    # Save the Excel file to the output directory with the given name
                    output_path = os.path.join(output_directory, f"{file_name}.xlsx")
                    with open(output_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Successfully downloaded {file_name}.xlsx")
                    break
                else:
                    print(f"Failed to download {file_name}. Status code: {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while downloading {file_name}: {e}")
            
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        
        if attempt == retries:
            print(f"Failed to download {file_name} after {retries} attempts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Excel files using file IDs and save with names from a text file.")
    parser.add_argument('input_file', help='Path to the text file containing file IDs and names')
    parser.add_argument('output_directory', help='Directory to save the downloaded Excel files')
    args = parser.parse_args()
    
    download_excel_files(args.input_file, args.output_directory)