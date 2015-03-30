import os
import os.path
from http_logging.http_logger import logger
from utils.git_commands import *
from utils.execute_commands import *

class EmptyLabActionError(Exception):
    pass
        
class LabActionScript:
    """Runs an action which is usually a bash or Python script."""
    ACTION_EMPTY        = 0x1
    ACTION_IN_PROGRESS  = 0x2
    ACTION_COMPLETED    = 0x4
    ACTION_UNSUCCESSFUL = 0x8

    INSTALL_SCRIPT_KEY      = "installer"

    ACTION_BUILD_KEY        = "build_steps"
    CONFIGURE_SCRIPT_KEY    = "configure"
    PRE_BUILD_SCRIPT_KEY    = "pre_build"
    BUILD_SCRIPT_KEY        = "build"
    POST_BUILD_SCRIPT_KEY   = "post_build"
    CHECK_STATUS_SCRIPT_KEY = "status"

    INIT_SCRIPT_KEY     = "init"
    START_SCRIPT_KEY    = "start"
    SHUTDOWN_SCRIPT_KEY = "shutdown"
    CLEAN_SCRIPT_KEY    = "clean"
    BACKUP_SCRIPT_KEY   = "backup"
    STATS_SCRIPT_KEY    = "stats"
    PUBLISH_SCRIPT_KEY  = "publish"
    
    def __init__(self, cmd):
        self._cmd = cmd.strip()
        self._state = LabActionScript.ACTION_EMPTY

    def run(self):
        """Runs a command. Waits for the command to finish."""
        if len(self._cmd) == 0:
            logger.error("LabActionScript::run() - No command to run")
            raise EmptyLabActionError("No command to run")
        try:
        	#self._cmd[0] = os.path.join(self._path_prefix, self._cmd[0])
            logger.debug("LabActionScript::run() - " + os.environ["http_proxy"])
            logger.debug("LabActionScript::run() - " + self._cmd)
            logger.debug("LabActionScript::run() - " + str(os.getcwd()))
            (ret_code, output) = execute_command(self._cmd)
            self._state = LabActionScript.ACTION_COMPLETED
        except Exception, e:
            self._state = LabActionScript.ACTION_UNSUCCESSFUL
            logger.error("LabActionScript::run() ose - " + str(ose))

        return self
    
    def run_async(self):
    	""" TODO: PROVIDE A DECENT IMPLEMENTATION!!"""
        """Runs a command asynchronously."""
        if self._cmd is None:
            raise EmptyLabActionError("No command to run")
        return self

    def empty(self):
        return self._state == LabActionScript.ACTION_EMPTY

    def done(self):
    	return self._state == LabActionScript.ACTION_COMPLETED

    def unsuccessful(self):
    	return self._state == LabActionScript.ACTION_UNSUCCESSFUL


if __name__ == '__main__':
    def testInvalidPathPrefix():
        action = LabActionScript("ls")
        action.run()
        print action._state
        assert(action.unsuccessful() == False)

    def testEmptyAction():
        try:
            action = LabActionScript("")
            action.run()
        except EmptyLabActionError:
            pass
        assert(action.empty() == True)
    
    def testGitCloneAction():
        action = LabActionScript("git clone https://bitbucket.org/deviprasad/itworkshop2-spring-2014.git")
        action.run()
        assert(action.done() == True)

    testInvalidPathPrefix()
    testEmptyAction()
    testGitCloneAction()
