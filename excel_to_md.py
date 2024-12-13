import os
import re
import openpyxl
import argparse

# Function to read pairs from an XLSX file
def get_pairs_from_xlsx(file_path):
    word_definition_pairs = []
    reverse_pairs = []

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if len(row) >= 3 and row[0] and row[1]:
            word = str(row[0]).strip()
            definition = str(row[2]).strip()
            word_definition_pairs.append(f"{word}::{definition}")
            reverse_pairs.append(f"{definition}::{word}")

    return word_definition_pairs, reverse_pairs

# Function to parse the existing MD file
def parse_md_file(md_path):
    with open(md_path, 'r') as file:
        content = file.read()

    # Extract tags and pairs
    flashcards_match = re.search(r'#flashcards/(\S+)', content)
    reverse_tag_exists = '[reverse]' in content
    reversed_tag_position = content.find('< reversed >')
    word_definition_pairs = re.findall(r'(\S+::.+?)(?=<!--SR:|\n|$)', content)
    sr_tags = re.findall(r'<!--SR:!(.*?)-->', content)

    return {
        "flashcards_tag": flashcards_match.group(1) if flashcards_match else None,
        "reverse_tag_exists": reverse_tag_exists,
        "reversed_tag_position": reversed_tag_position,
        "word_definition_pairs": word_definition_pairs,
        "sr_tags": sr_tags,
    }

# Function to update or create the MD file
def update_md_file(md_path, base_name, word_definition_pairs, reverse_pairs):
    if not os.path.exists(md_path):
        with open(md_path, 'w') as file:
            file.write(f"#flashcards/{base_name}\n")
            file.write("[reverse]\n")
            file.write("< reversed >\n")

    print("New word definition pairs: {}".format(word_definition_pairs))
    print("New reversed word definition pairs: {}".format(reverse_pairs))

    parsed_data = parse_md_file(md_path)

    with open(md_path, 'r') as file:
        content = file.read()

    # Insert word::definition pairs before < reversed >
    new_content = content
    if parsed_data["reversed_tag_position"] != -1:
        before_reversed = content[:parsed_data["reversed_tag_position"]]
        after_reversed = content[parsed_data["reversed_tag_position"]:]

        print("Original content before reversed: {}".format(before_reversed))
        print("Original content after reversed: {}".format(after_reversed))

        for pair in word_definition_pairs:
            if pair not in before_reversed:
                before_reversed += f"\n{pair}"

        for pair in reverse_pairs:
            if pair not in after_reversed:
                after_reversed += f"\n{pair}"

        new_content = "{}\n{}".format(before_reversed, after_reversed)
    else:
        before_reversed = content[:parsed_data["reversed_tag_position"]]

        for pair in word_definition_pairs:
            if pair not in before_reversed:
                before_reversed += f"\n{pair}"

        new_content = before_reversed


    with open(md_path, 'w') as file:
        file.write(new_content)

# Main function to process files
def process_excel_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.xlsx'):
            base_name = os.path.splitext(filename)[0]
            xlsx_path = os.path.join(input_dir, filename)
            md_path = os.path.join(output_dir, f"{base_name}.md")

            word_definition_pairs, reverse_pairs = get_pairs_from_xlsx(xlsx_path)
            update_md_file(md_path, base_name, word_definition_pairs, reverse_pairs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Excel files to text .md files in a given directory.")
    parser.add_argument('input_directory', help='Directory containing Excel files to process')
    parser.add_argument('output_directory', help='Directory to save the generated .md files')
    args = parser.parse_args()

    process_excel_files(args.input_directory, args.output_directory)