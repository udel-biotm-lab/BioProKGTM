import os

def process_files(input_directory, output_directory):
    # Create the output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all files in the given directory that match the pattern 'output_*.txt'
    files = [f for f in os.listdir(input_directory) if f.startswith('output_') and f.endswith('.txt')]
    
    for file in files:
        file_path = os.path.join(input_directory, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Remove completely blank lines and then ensure lines end with a period if they do not already.
        filtered_lines = [line for line in lines if line.strip() != '']  # Remove blank lines
        lines = [line.strip() + ('' if line.strip().endswith('.') else '.') + '\n' for line in filtered_lines]

        # Get the base part number from the filename, excluding extension
        base_part_number = file.split("_")[1].split('.txt')[0]

        # Check if the file needs to be split.
        if len(lines) > 150:
            # Split the file into chunks of 150 lines each.
            for i in range(0, len(lines), 150):
                part_number = (i // 150) + 1
                new_file_path = os.path.join(output_directory, f'chapter_{base_part_number}_{part_number}.txt')
                with open(new_file_path, 'w') as new_file:
                    new_file.writelines(lines[i:i+150])
        else:
            # Rename the file directly if no splitting is needed.
            new_file_path = os.path.join(output_directory, f'chapter_{base_part_number}.txt')
            with open(new_file_path, 'w') as new_file:
                new_file.writelines(lines)


# Example usage
input_dir = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Book'
output_dir = '/home/shovan/nlputils/EDG_framework/Lexical_Concepts/Input_Text_File/Processed_Text_Book'
process_files(input_dir, output_dir)
