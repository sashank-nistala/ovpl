""" 
This is a sample client script, which shows how HTTP Request 
can be made using HTTPClientRequest 
"""

import sys
import os
import re
import logging

from HTTPClientRequest import *

HOST_NAME = 'http://localhost'
PORT_NUMBER = '8089'

valid_json_file_name = r'[a-zA-Z0-9\-]+\.json'

if len(sys.argv) != 2:
    logging.critical('One of the input parameter is missing! Exiting the program')
    sys.exit()
else:
    if not bool(re.match(valid_json_file_name, sys.argv[1])):
        logging.error('Invalid JSON file')
        sys.exit()
    else:  
        fn = open(sys.argv[1], 'r')
        json_file = fn.read()
        fn.close()


if __name__ == '__main__':
        my_request = HTTPClientRequest(json_file, HOST_NAME, PORT_NUMBER)
        response = my_request.execute()
        print response.read()