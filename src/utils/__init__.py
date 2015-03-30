import os
import sys

def set_import_search_path():
    # The assumption here is that this script is in the src directory
    # which is one directory above ovpl
    ovpl_directory_path = os.path.dirname(os.path.abspath(__file__))
    path_list = ovpl_directory_path.split("/")
    path_list1 = path_list[:-2] # remove src - till ovpl
    path_list2 = path_list[:-1] # src included - till ovpl/src
    
    ovpl_directory_path1 = "/".join(path_list1)
    ovpl_directory_path2 = "/".join(path_list2)
    
    sys.path.append(ovpl_directory_path1)
    sys.path.append(ovpl_directory_path2)
     
set_import_search_path()


    
    
