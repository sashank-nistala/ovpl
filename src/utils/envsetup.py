import os
import sys
import netaddr
import json
from adapters.settings import get_subnet

class EnvSetUp:

    def __init__(self):
        #do nothing
        self.ovpl_directory_path = None
        self.config_spec = None
        self.http_proxy =  None
        self.https_proxy = None
        self.no_proxy = ""
        self.set_ovpl_directory_path()
        self.setup_pythonpath()
        self.create_no_proxy_string()
        self.get_proxy_values()
        self.set_environment()
        
    def set_ovpl_directory_path(self):
        # The assumption here is that this script is in the src directory
        # which is one directory above ovpl
        self.ovpl_directory_path = os.path.dirname(os.path.abspath(__file__))
        path_list = self.ovpl_directory_path.split("/")
        path_list = path_list[:-2] # remove 'utils' and 'src' from the list
        self.ovpl_directory_path = "/".join(path_list)

    def get_ovpl_directory_path(self):
        return self.ovpl_directory_path
        
    def setup_pythonpath(self):
        sys.path.append(self.ovpl_directory_path)

    def create_no_proxy_string(self):
        
        for subnet in get_subnet():
            parts = subnet.split(".")
            parts[2] = parts[3] = "0"
            self.no_proxy = ".".join(parts) + "/16,"

        self.no_proxy += "localhost"


    def get_proxy_values(self):
        self.config_spec = json.loads(open(self.ovpl_directory_path + "/config/config.json").read())
        self.http_proxy  = self.config_spec["ENVIRONMENT"]["HTTP_PROXY"]
        self.https_proxy = self.config_spec["ENVIRONMENT"]["HTTPS_PROXY"]

    def set_environment(self):
        os.environ["http_proxy"] = self.http_proxy
        os.environ["https_proxy"] = self.https_proxy
        os.environ["no_proxy"] = self.no_proxy
        if "PYTHONPATH" in os.environ:
            if self.ovpl_directory_path not in os.environ["PYTHONPATH"]:
                os.environ["PYTHONPATH"] += ":"
                os.environ["PYTHONPATH"] += self.ovpl_directory_path
        else:
            os.environ["PYTHONPATH"] = self.ovpl_directory_path

            
if __name__ == '__main__':
    e = EnvSetUp()
#    print e.ovpl_directory_path
#    print e.no_proxy
#    print e.http_proxy
#    print e.https_proxy
    print os.environ["http_proxy"]
    print os.environ["https_proxy"]
    print os.environ["no_proxy"]
    print os.environ["PYTHONPATH"]
