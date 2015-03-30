class BaseAdapter:
	def create_vm(lab_spec):
		raise Exception("BaseAdapter: unimplemented create_vm()")

	def init_vm(vm_id, lab_repo_name):
		raise Exception("BaseAdapter: unimplemented init_()")
		return (False, "unimplemented") #success status, response string


import netaddr
import sh
import json

import settings
from http_logging.http_logger import logger
from utils.envsetup import EnvSetUp


e = EnvSetUp()
try:
    config_spec = json.loads(open(e.get_ovpl_directory_path() + "/config/config.json").read())
except IOError as e:
    logger.error("unable to load config.json. Exception: " + str(e))
    raise e
except  Exception as e:
    logger.error("unable to parse config.json. Exception: " + str(e))


# tries to find if a specific IP is given in the config file
def get_ip_from_config():
    global config_spec
    try:
        ip = config_spec['CONTAINER_CONFIG']['STATIC_IP_ADD']
    except KeyError:
        logger.debug("Key Error, IP not found")
        return (False, "0.0.0.0")

    if not ip or type(ip) is not str:
        return (False, "0.0.0.0")

    
    return (True, ip)

#returns a free ip as a string for a container to bind to.
def find_available_ip():
    # check first to see if this is using single, static IP for containers
    # then return that only; else try to find new IP dynamically.
    (ret_val, ip) = get_ip_from_config()
    logger.debug("return value = %r, ip = %s" % (ret_val, ip))
    if (ret_val): #returned true
        return ip

    #try and ping. if the IP does not respond, (gives wrong return code) return the IP as free
    def is_ip_free(ip):
        try:
            sh.ping(str(ip), c=1)
        except sh.ErrorReturnCode:
            return True

        return False

    def is_ip_usable(ip):
            #reject IP's like  192.0.2.0 or 192.0.2.255 for subnet 192.0.2.0/24
            return not (ip == ip_network.network or ip == ip_network.broadcast)

    for subnet in settings.get_subnet():
        ip_network = netaddr.IPNetwork(subnet)
        ip_addrs = list(ip_network)
        #logger.debug("ip addresses: %s" % str(ip_addrs))
        for ip in ip_addrs:
            if is_ip_usable(ip) and is_ip_free(ip):
                return str(ip)

    raise Exception("unable to find free ip in subnet ", settings.get_subnet())
    return None
