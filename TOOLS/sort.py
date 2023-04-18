import os

# Define the directory path and the dictionary containing the expected number of files in each folder
dir_path = "../CONTENTS"
sort = '/Users/faketiml/Downloads/Zhihu-VIP/CATEGORIES'

# Append book under category
def sort_book(dir):
    with open(f'{dir}/README.md', 'r') as file:
        lines = file.readlines()
        title = lines[0][2:-1]
        cats = lines[4][7:-1].split(' · ')
    for cat in cats:
        with open(f'{sort}/.temp/{cat}.md', 'a') as file:
            file.write('\n- [%s](../CONTENTS/%s/README.md)' %
                        (title, title.replace(' ', '%20')))

os.mkdir(f'{sort}/.temp')
# Loop through the immediate subdirectories of the directory path
for folder_name in os.listdir(dir_path):
    folder_path = os.path.join(dir_path, folder_name)

    if os.path.isdir(folder_path):
      sort_book(folder_path)

for filename in os.listdir(f'{sort}'):
  if filename.endswith('.md'):
    os.remove(f'{sort}/{filename}')

for filename in os.listdir(f'{sort}/.temp'):
  os.rename(f'{sort}/.temp/{filename}', f'{sort}/{filename}')
  
os.rmdir(f'{sort}/.temp')
