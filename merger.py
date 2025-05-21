import os

def merge_code_to_file(file_paths, output_file="merged_code.txt"):
    """
    Merges the content of multiple code files into a single text file.

    Args:
        file_paths (list): A list of paths to the HTML, CSS, Python,
                           and JavaScript files to be merged.
        output_file (str): The name of the output text file.
                           Defaults to "merged_code.txt".
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    outfile.write(f"-- Start of file: {file_path} --\n")
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    outfile.write(f"\n-- End of file: {file_path} --\n\n")
                else:
                    print(f"Warning: File not found: {file_path}")
        print(f"Successfully merged code into: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    files_to_merge = [
        "login.html",  # Replace with your HTML file path
        "styles.css",  # Replace with your CSS file path
        "script.js",   # Replace with your JavaScript file path
        "validation.py"      # Replace with your Python file path
        # Add more file paths as needed
    ]
    merge_code_to_file(files_to_merge)