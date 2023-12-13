import os
from datetime import datetime

def get_directory_sizes(path):
    date_string = datetime.now().strftime('%d%m%Y-%H')
    print(date_string)

    with open(f'{date_string}-size-output.txt', 'w') as output_file, open(f'{date_string}-over5GB.txt', 'w') as over5GB_file:
        for dirpath, dirnames, filenames in os.walk(path):
            total_size = 0

            # Calculate the size of files in the current directory
            for filename in filenames:
                fp = os.path.join(dirpath, filename)
                total_size += os.path.getsize(fp)

            # Include the size of the current directory itself
            total_size += os.path.getsize(dirpath)

            # Print the directory and its size to the output file
            output_file.write(f"Directory: {dirpath} - Size: {total_size} bytes\n")

            # Check if the total size is over 5GB (5 * 1024 * 1024 * 1024 bytes)
            if total_size > 5 * 1024 * 1024 * 1024:
                over5GB_file.write(f"Directory: {dirpath} - Size: {total_size} bytes\n")

get_directory_sizes('C:\\')
