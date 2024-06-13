import sys
import os
import subprocess

if len(sys.argv) != 3:
    print("Usage: python script_name.py <directory> <output_file>")
    sys.exit(1)

# Directory containing your text files and the output file path from command line arguments
directory = sys.argv[1]
output_file = sys.argv[2]

# Open the output file for writing
with open(output_file, "w") as outfile:
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            # Write the file name to the output file
            outfile.write(f"Processing file: {file_path}\n")

            # Execute your command and capture the output
            process = subprocess.run(["./identify_abbr", file_path], capture_output=True, text=True)
            # Write the command output to the output file
            outfile.write(process.stdout + "\n")

print(f"Processing completed. Results are in {output_file}.")
