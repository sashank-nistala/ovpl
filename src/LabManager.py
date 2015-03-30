import json
import re
import os
import os.path
from exceptions import Exception
import requests
import time
import math

from http_logging.http_logger import logger
from utils.envsetup import EnvSetUp
from utils.git_commands import * 
import ads_to_dataservices
from ads_to_dataservices import update_status

def get_lab_reqs(lab_src_url, version=None):

    e = EnvSetUp()	
    logger.debug("Will return lab spec")

    try:
        repo_name = construct_repo_name(lab_src_url)
        if repo_exists(repo_name):
    #       reset_repo(repo_name)
            pull_repo(repo_name)
        else:
            clone_repo(lab_src_url, repo_name)

        checkout_version(repo_name, version)
        return get_lab_spec(repo_name)
    except Exception, e:
        logger.error("Error: %s" % str(e))
        raise e

def test_lab(vmmgr_ip, port, lab_src_url, version=None):
    # make sure VM Manager is running
    # the target VM should have LabActionRunner scripts 
    # VM Manager should do the following?
    # or better it should invoke another script which should
        # clone the repo in the VM
        # get the lab_spec
        # run Lab Action Runner
    if not 'http' in vmmgr_ip:
        raise Exception('Protocol not specified in VMManager host address!!')

    e = EnvSetUp()
    logger.debug("vmmgr_ip = %s, port = %s, lab_src_url = %s" % (vmmgr_ip, port, lab_src_url))
    payload = {"lab_src_url": lab_src_url, "version": version}
    config_spec = json.loads(open(e.get_ovpl_directory_path() + "/config/config.json").read())
    TEST_LAB_API_URI = config_spec["VMMANAGER_CONFIG"]["TEST_LAB_URI"]
    url = '%s:%s%s' % (vmmgr_ip, port, TEST_LAB_API_URI)
    logger.debug("url = %s, payload = %s" % (url, str(payload)))
    if type(ads_to_dataservices.lab_id_deployed) is int: 			
    	update_status(ads_to_dataservices.lab_id_deployed,2)

    exception_str = ""
    for i in (1,2,4,8,16):
        time.sleep(i)
        try:
            response = requests.post(url=url, data=payload)
            logger.debug("response = %s" % response)
            return ("Success" in response.text, response.text)
        except Exception, e:
            exception_str = str(e)
            attempts = {0:'first', 1:'second', 2:'third', 3:'fourth'}
            logger.error("Error installing lab on VM for the %s attempt with error: %s" % \
                                 (attempts[math.log(i)/math.log(2)], str(e)))
    return (False, exception_str)
    
if __name__ == '__main__':

    try:
        lab_spec = get_lab_reqs('https://bitbucket.org/virtual-labs/cse02-programming.git', version=None)
        logger.debug("Lab spec: %s" % str(lab_spec))
    except Exception, e:
        logger.error("Test failed with error: " + str(e))

'''
    (ret_val, ret_str) = test_lab('http://10.2.58.130', '9089', 'https://bitbucket.org/virtual-labs/cse02-programming.git')
    if (ret_val):
        logger.debug("Test Successful, ret_val = %s, ret_str = %s" % (str(ret_val), ret_str))
    else:
        logger.debug("Test UnSuccessful, ret_val = %s, ret_str = %s" % (str(ret_val), ret_str))
'''



    
   
