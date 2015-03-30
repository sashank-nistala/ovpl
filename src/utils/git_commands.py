import os
import json
import __init__
from http_logging.http_logger import logger
from utils.execute_commands import *
from utils.envsetup import EnvSetUp

e = EnvSetUp()
config_spec = json.loads(open(e.get_ovpl_directory_path() + "/config/config.json").read())
GIT_CLONE_LOC =  config_spec["LABMANAGER_CONFIG"]["GIT_CLONE_LOC"]
LAB_SPEC_DIR =  config_spec["LABMANAGER_CONFIG"]["LAB_SPEC_DIR"]
LAB_SPEC_FILE =  config_spec["LABMANAGER_CONFIG"]["LAB_SPEC_FILE"]
logger.debug("GIT_CLONE_LOC = %s" % str(GIT_CLONE_LOC))
logger.debug("LAB_SPEC_DIR = %s" % str(LAB_SPEC_DIR))
logger.debug("LAB_SPEC_FILE = %s" % str(LAB_SPEC_FILE))

class LabSpecInvalid(Exception):
    def __init__(self, msg):
        Exception(self, msg)

# sample lab_src_url: git@github.com:vlead/ovpl.git
def construct_repo_name(lab_src_url):
    logger.debug("lab_src_url: %s" % lab_src_url)
    repo = lab_src_url.split('/')[-1]
    repo_name = (repo[:-4] if repo[-4:] == ".git" else repo)
    logger.debug("repo_name: %s" % repo_name)
    return str(repo_name)

def repo_exists(repo_name):
    return os.path.isdir(GIT_CLONE_LOC+repo_name)

def clone_repo(lab_src_url, repo_name):
    clone_cmd = "git clone %s %s%s" % (lab_src_url, GIT_CLONE_LOC,repo_name)
    logger.debug(clone_cmd)
    logger.debug("http_proxy: %s" % os.environ['http_proxy'])
    logger.debug("https_proxy: %s" % os.environ['https_proxy'])
    try:
        (ret_code, output) = execute_command(clone_cmd)
        logger.debug("Clone repo successful")
    except Exception, e:
        logger.error("Error Cloning the repository: " + str(e))
        raise e
            

def pull_repo(repo_name):
    pull_cmd = "git --git-dir=%s/.git pull" % (GIT_CLONE_LOC + repo_name)
    logger.debug("pull cmd: %s" % pull_cmd)
    try:
        (ret_code, output) = execute_command(pull_cmd)
        logger.debug("Pull repo successful")
    except Exception, e:
        logger.error("Error Pulling the repository: " + str(e))
        raise e

def reset_repo(repo_name):
    reset_cmd = "git --git-dir=%s/.git reset --hard" % (GIT_CLONE_LOC + repo_name)
    logger.debug("reset cmd: %s" % reset_cmd)
    try:
        (ret_code, output) = execute_command(reset_cmd)
        logger.debug("reset repo successful")
    except Exception, e:
        logger.error("Error Resetting the repository: " + str(e))
        raise e

def checkout_version(repo_name, version=None):
    if version:
        checkout_cmd = "git --git-dir=%s checkout %s" \
            % ((GIT_CLONE_LOC + repo_name), version)
        try:
            (ret_code, output) = execute_command(reset_cmd)
            logger.debug("reset repo successful")
        except Exception, e:
            logger.error("Error Resetting the repository: " + str(e))
            raise e
        
def get_spec_path(repo_name):
    return GIT_CLONE_LOC + repo_name + LAB_SPEC_DIR

def get_lab_spec(repo_name):
    spec_file_path = get_spec_path(repo_name) + LAB_SPEC_FILE
    logger.debug("spec_file_path: %s" % spec_file_path)
    if not os.path.exists(spec_file_path):
        logger.error("Lab spec file not found")
        raise LabSpecInvalid("Lab spec file not found")
    try:
        return json.loads(open(spec_file_path).read())
    except Exception, e:
        logger.error("Lab spec JSON invalid: " + str(e))
        raise LabSpecInvalid("Lab spec JSON invalid: " + str(e))


if __name__ == '__main__':
    clone_repo("https://bitbucket.org/virtual-labs/cse02-programming.git", "cse02-programming")
