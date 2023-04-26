# Checks the number of files of every book against the declared chapters

import os

def get_info(dir):
    with open(f'{dir}/README.md', 'r') as file:
      lines = file.readlines()
    # Compare status
    status = lines[6][7:-1]
    end = status.find('节')
    # URL
    url = lines[10][9:-1]
    return int(status[6:end-1]), url

def clean(dir):
    with open(f'{dir}/README.md', 'r') as file:
      lines = file.readlines()
    
    try:
      os.mkdir(f'{dir}/.temp')
      os.rename(f'{dir}/README.md', f'{dir}/.temp/README.md')

      for i in range(len(lines)-1, 0, -1):
        line = lines[i]
        if line.startswith('## 目录'):
            break
        end = line.find(')<!--')
        if end < 0:
          end = -2 if line[-1]=='\n' else -1
        filename = line[line.index('](')+2:end].replace('%20', ' ')
        os.rename(f'{dir}/{filename}', f'{dir}/.temp/{filename}')
      print(f'{len(os.listdir(f"{dir}/.temp"))-1} files filtered.')
      for filename in os.listdir(f'{dir}'):
        if filename.endswith('.md'):
          os.remove(f'{dir}/{filename}')
      print('Cleaned.')
    finally:
      for filename in os.listdir(f'{dir}/.temp'):
        os.rename(f'{dir}/.temp/{filename}', f'{dir}/{filename}')
      os.rmdir(f'{dir}/.temp')
    
def handle(dir, url):
    os.system(f"open '{dir}'")
    print(dir)
    print(url)
    if input('Clean? (y/n) ') == 'y':
      clean(dir)
      input('Press Enter to continue...')

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
            count, url = get_info(folder_path)
          # Check if the actual number of files matches the expected number
            if file_count != count + 1:
              print(f'Record: {count}; Actual: {file_count-1}')
              raise Exception()
        except:
            handle(folder_path, url)
print('Check complete.')
