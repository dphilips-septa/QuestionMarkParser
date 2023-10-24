import os
import shutil
path_of_all_tests = 'All Tests'
dir_list = os.listdir(path_of_all_tests)
new_dir_list = dir_list.copy()

for i in range(len(dir_list)):
    if ' .html' in dir_list[i]:
        print('replaced')
        new_dir_list[i] = new_dir_list[i].replace(' .html','.html')


folder_names = [a.split('.')[0] for a in new_dir_list]

for i in range(len(folder_names)):
    print(f'Resetting folder for {dir_list[i]}')
    try:
        shutil.copyfile(f'{path_of_all_tests}/{dir_list[i]}',f'All Tests Data/{folder_names[i]}/{new_dir_list[i]}')
    except:
        os.mkdir(f'All Tests Data/{folder_names[i]}')
        shutil.copyfile(f'{path_of_all_tests}/{dir_list[i]}',f'All Tests Data/{folder_names[i]}/{new_dir_list[i]}')
