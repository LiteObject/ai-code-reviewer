"""
Delete all folders in a directory that contain the string 'node_modules'.
"""

import os
import time
import shutil
from multiprocessing import Pool
from itertools import cycle

TARGET_ROOT_FOLDER = '../../LiteObject'
FIND_FOLDER = 'node_modules'
start_time = time.time()
#deleted_file_count = 0

def get_folders_to_delete(target_folder, find_folder, exclude_folders):
    """
    Get a list of folders to delete.
    :param target_folder: Folder to search.
    :param delete_folder_list: Folder name to search for.
    :return: List of folders to delete.
    """
    delete_list = []
    for root, dirs, files in os.walk(target_folder):
        if find_folder in dirs and all(exclude_folder not in root for exclude_folder in exclude_folders):
            delete_list.append(os.path.join(root, find_folder))
    return delete_list

def delete_folder(folder):
    """
    Delete a folder and all its contents.
    :param folder: Folder to delete.
    :return: None.    
    """
    # os.remove(node_modules_path) # <- Needs to run as an admin/with elevated privilages?
    try:
        print(f"Deleting {folder}", end="")
        spinner = cycle(["-", "\\", "|", "/"])
        while True:
            print(next(spinner), end="\r")
            time.sleep(0.1)
            try:
                shutil.rmtree(folder)
                print(f"Deleted {folder}")
                break
            except FileNotFoundError as e:
                print(f'Error: {folder}. {e!r}')
                break
        # deleted_file_count += 1
    except FileNotFoundError as e:
        print(f'Error: {folder}. {e!r}')

end_time = time.time()
total_time = end_time - start_time

#print(f"Deleted {deleted_file_count} files, Total runtime: {total_time} seconds")

if __name__ == '__main__':
    print('>>> Invoked main function')
    pool = Pool()
    EXCLUDE_FOLDERS = ['python-exercise']
    folders_to_delete_list = get_folders_to_delete(TARGET_ROOT_FOLDER, FIND_FOLDER, EXCLUDE_FOLDERS)
    lst = pool.map(delete_folder, folders_to_delete_list)
    pool.close()
    pool.join()
