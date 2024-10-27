import pandas as pd
import os
import argparse

def process_excel_files(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate over all Excel files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".xlsx"):
            input_path = os.path.join(input_directory, filename)
            
            # Extract the base name without extension for the output file
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_directory, f"{base_name}.md")
            
            # Read the Excel file
            df = pd.read_excel(input_path)

            # Read existing content from the .md file (if it exists) to avoid duplicates
            existing_content = set()
            if os.path.exists(output_path):
                with open(output_path, 'r') as f:
                    for line in f:
                        existing_content.add(line.strip())
            
            # Open the .md file to append only new lines
            with open(output_path, 'a') as f:
                # Skip the first row by using df.iloc[1:]
                for index, row in df.iloc[1:].iterrows():
                    # Assuming 'A' and 'C' are the names of the columns
                    new_line = f"{row[0]}::{row[2]}"
                    if new_line not in existing_content:
                        f.write(new_line + "\n")
                        existing_content.add(new_line)
            
            print(f"Processed {filename} into {base_name}.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Excel files to text .md files in a given directory.")
    parser.add_argument('input_directory', help='Directory containing Excel files to process')
    parser.add_argument('output_directory', help='Directory to save the generated .md files')
    args = parser.parse_args()
    
    process_excel_files(args.input_directory, args.output_directory)
