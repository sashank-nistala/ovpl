import os
import sys

def set_import_search_path():
    # The assumption here is that this script is in the src directory
    # which is one directory above ovpl
    ovpl_directory_path = os.path.dirname(os.path.abspath(__file__))
    path_list = ovpl_directory_path.split("/")
    path_list = path_list[:-1] # remove 'adapters and 'src' from the list
    ovpl_directory_path = "/".join(path_list)
    print ovpl_directory_path
    sys.path.append(ovpl_directory_path)


set_import_search_path()


    
    
