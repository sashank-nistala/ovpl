import os
import subprocess
import json
import __init__
from http_logging.http_logger import logger
from utils.envsetup import EnvSetUp

# Backporting check_output from 2.7 to 2.6
if "check_output" not in dir(subprocess):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

def execute_command(cmd):
    e = EnvSetUp()
    logger.debug("command: %s" % cmd)
    return_code = -1
    output = None
    try:
        output = subprocess.check_output(cmd, shell=True)
        return_code = 0
    except subprocess.CalledProcessError as cpe:
        logger.error("Called Process Error: %s" % cpe)
        raise cpe
    except OSError as ose:
        logger.error("OSError: %s" % ose)
        raise ose

    return (return_code, output)

if __name__ == '__main__':
    try:
        execute_command("git clone https://bitbucket.org/virtual-labs/cse02-programming.git /root/labs/cse02-programming")
    except Exception, e:
        logger.error("command execution failed: %s" % str(e))
