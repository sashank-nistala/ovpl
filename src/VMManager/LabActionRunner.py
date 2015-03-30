import json
from http_logging.http_logger import logger
from LabActionScript import LabActionScript


class LabActionRunner:
    """
    
    An 'action' is an abstract operation in the life cycle of a lab.
    Each action consists of one or more 'step's.
    Each step involves the execution of zero or more 'scripts'.

    For example, the 'build' action has five steps: configure, pre_build, build, post_build, status.
    Each of these steps may require the execution of zero or more scripts.

    This object is driven by the lab-requirements specification.

    """
    def __init__(self, actions, path_prefix=""):
        self._actions = actions
        self._path_prefix = path_prefix
  #      logger.debug("CWD: %s" % str(os.getcwd()))


    def _run_(self, scripts):
        for a in scripts:
            #print "command:<" + a + ">"
            script = LabActionScript(a)
            script.run()
            if script.unsuccessful():
                raise Exception("Script " + a + " failed")
    
    def _run_action_(self, action_id):
    	if not self._actions is None and self._actions.has_key(action_id):
    	    self._run_(self._actions[action_id]) # array of scripts to run wrt this action
    
    # actions that build lab source code within a VM.
    # checkout, install dependencies, configure and build the lab sources.
    def run_install_source(self):
        if not self._actions is None and self._actions.has_key(LabActionScript.INSTALL_SCRIPT_KEY):
            self._run_(self._actions[LabActionScript.INSTALL_SCRIPT_KEY])
    
    def run_build_steps(self):
    	if self._actions is None or not self._actions.has_key(LabActionScript.ACTION_BUILD_KEY):
    		return 0
        build_steps = self._actions[LabActionScript.ACTION_BUILD_KEY]

        def configure(steps):
            logger.info("Configuring the lab...")
            if steps.has_key(LabActionScript.CONFIGURE_SCRIPT_KEY):
    	        self._run_(steps[LabActionScript.CONFIGURE_SCRIPT_KEY])
        
        def pre_build(steps):
            logger.info("Running the pre-build scripts...")
            if steps.has_key(LabActionScript.PRE_BUILD_SCRIPT_KEY):
    	        self._run_(steps[LabActionScript.PRE_BUILD_SCRIPT_KEY])
        
        def build(steps):
            logger.info("Running the build scripts...")
            if steps.has_key(LabActionScript.BUILD_SCRIPT_KEY):
    	        self._run_(steps[LabActionScript.BUILD_SCRIPT_KEY])
        
        def post_build(steps):
            logger.info("Running the post-build scripts...")
            if steps.has_key(LabActionScript.POST_BUILD_SCRIPT_KEY):
    	        self._run_(steps[LabActionScript.POST_BUILD_SCRIPT_KEY])

        def status(steps):
            logger.info("Checking the status of the build...")
            if steps.has_key(LabActionScript.CHECK_STATUS_SCRIPT_KEY):
    	        return self._run_(steps[LabActionScript.CHECK_STATUS_SCRIPT_KEY])
            return 0
        
        configure(build_steps)
        pre_build(build_steps)
        build(build_steps)
        post_build(build_steps)
        return status(build_steps)

    # actions that correspond with the runtime states of a lab
    def run_init_lab(self):
        logger.debug("LabActionRunner::run_init_lab()")
    	self._run_action_(LabActionScript.INIT_SCRIPT_KEY)

    def run_start_lab(self):
        logger.debug("LabActionRunner::run_start_lab()")
    	self._run_action_(LabActionScript.START_SCRIPT_KEY)

    def run_shutdown_lab(self):
        logger.debug("LabActionRunner::run_shutdown_lab()")
    	self._run_action_(LabActionScript.SHUTDOWN_SCRIPT_KEY)

    def run_clean_lab(self):
        logger.debug("LabActionRunner::run_clean_lab()")
    	self._run_action_(LabActionScript.CLEAN_SCRIPT_KEY)
    
    def run_backup_lab(self):
        logger.debug("LabActionRunner::run_backup_lab()")
    	self._run_action_(LabActionScript.BACKUP_SCRIPT_KEY)

    def run_stats_lab(self):
        logger.debug("LabActionRunner::run_stats_lab()")
    	self._run_action_(LabActionScript.STATS_SCRIPT_KEY)

    def run_publish_lab(self):
        logger.debug("LabActionRunner::run_publish_lab()")
    	self._run_action_(LabActionScript.PUBLISH_SCRIPT_KEY)


if __name__ == '__main__':
	def tests():
	    def testInitActions():
	        init_action_spec = '{"init": ["scripts/on_init_lab.sh", "scripts/first_run.py --silent", "scripts/start_services.sh"]}'
	        lar = LabActionRunner(json.loads(init_action_spec), "")
	        #lar.display()
	        lar.run_init_lab()
	        
	    def testEmptyBuildActions():
	    	build_steps_spec = '{}'
	    	lar = LabActionRunner(json.loads(build_steps_spec), "")
	        lar.run_build_steps()
	    
	    def testEmptyBuildStepActions():
	    	build_steps_spec = '{"build_steps": {}}'
	    	lar = LabActionRunner(json.loads(build_steps_spec), "")
	        lar.run_build_steps()
	    
	    def testEmptyConfigureBuildStepActions():
	    	build_steps_spec = '{"build_steps": {"configure": []}}'
	    	lar = LabActionRunner(json.loads(build_steps_spec), "")
	        lar.run_build_steps()

	    def testBuildActions():
	        build_steps_spec = '{"build_steps": { "configure": ["scripts/configure.sh", "/bin/ls -l"], "pre_build": ["make clean"], "build": ["make lab", "make install"], "post_build": ["make clean"], "status": ["scripts/check_build_status.sh"]}}'
	        lar = LabActionRunner(json.loads(build_steps_spec), "")
	        lar.run_build_steps()
	        #print json.loads(build_steps_spec)

	    def testEmpty():
	        installer_steps_spec = '{}'
	        lar = LabActionRunner(json.loads(installer_steps_spec), "")
	        lar.run_install_source()

	    def testEmptyInstallSources():
	        installer_steps_spec = '{"installer": []}'
	        lar = LabActionRunner(json.loads(installer_steps_spec), "")
	        lar.run_install_source()

	    def testInstallSources():
	        installer_steps_spec = '{"installer": [ "sudo apt-get install libxml24", "sudo apt-get install libnss34", "sudo apt-get install python2.74", "sudo apt-get install curl4", "git clone https://bitbucket.org/deviprasad/data_structures.git", "wget -b -O output/log.txt --user=witcracker --password=secretpassword www.myhome.in/config_lab.py"]}'
	        lar = LabActionRunner(json.loads(installer_steps_spec), "")
	        lar.run_install_source()

	    testEmpty()
	    testEmptyInstallSources()
	    testInstallSources()
	    testInitActions()
	    testEmptyBuildActions()
	    testEmptyBuildStepActions()
	    testEmptyConfigureBuildStepActions()
	    testBuildActions()

	tests()
