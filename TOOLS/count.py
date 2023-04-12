# Checks the number of files of every book against the declared chapters

import os

def get_number(dir):
    with open(f'{dir}/README.md', 'r') as file:
      lines = file.readlines()
    # Compare status
    status = lines[6][7:-1]
    end = status.find('节')
    return int(status[6:end-1])

# Define the directory path and the dictionary containing the expected number of files in each folder
dir_path = "../CONTENTS"

# Loop through the immediate subdirectories of the directory path
for folder_name in os.listdir(dir_path):
    folder_path = os.path.join(dir_path, folder_name)

    # Check if the subdirectory is a directory (not a file) and matches an entry in the dictionary
    if os.path.isdir(folder_path):
        try:
          os.remove(os.path.join(folder_path, '.DS_Store'))
        except:
          pass
        # Count the number of files in the folder
        file_count = len(os.listdir(folder_path))

        try:
          # Check if the actual number of files matches the expected number
            if file_count != get_number(folder_path) + 1:
              os.system(f"open '{folder_path}'")
              exit()
        except:
            os.system(f"open '{folder_path}'")
            exit()
