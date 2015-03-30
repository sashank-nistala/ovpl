"""
VMPoolManager manages a set of VMPools i.e. maintain a list of available VMPools
and decide which VMPool to use for creating a VM.
"""
import json
import os.path

import VMPool
from http_logging.http_logger import logger
from State import State
from utils.envsetup import EnvSetUp

class VMPoolManager:

    def __init__(self):
        """ State should be rewriten"""
        logger.debug("VMPoolManager: _init_()")
        self.system = State.Instance()
        
        self.VMPools = []
        e = EnvSetUp()
        config_spec = json.loads(open(e.get_ovpl_directory_path() + "/config/config.json").read())
        pools = config_spec["VMPOOL_CONFIGURATION"]["VMPOOLS"]
        create_uri = config_spec["API_ENDPOINTS"]["CREATE_URI_ADAPTER_ENDPOINT"]
        destroy_uri = config_spec["API_ENDPOINTS"]["DESTROY_URI_ADAPTER_ENDPOINT"]

        for pool in pools:
            self.add_vm_pool( pool["POOLID"], \
                              pool["DESCRIPTION"], \
                              pool["ADAPTERIP"], \
                              pool["PORT"], \
                              create_uri,  \
                              destroy_uri)

        logger.debug("VMPoolManager: _init_();  vm_pools = %s" % (str(self.VMPools)))


    def add_vm_pool(self, vm_pool_id, vm_description, adapter_ip, adapter_port, create_path, destroy_path):
        logger.debug("VMPoolManager: add_vm_pool(); %s, %s, %s, %s, %s, %s" % \
                             (vm_pool_id, vm_description, adapter_ip, adapter_port, create_path, destroy_path))
        self.VMPools.append(VMPool.VMPool(vm_pool_id, vm_description, adapter_ip, adapter_port, create_path, destroy_path))

    def get_available_pool(self, lab_spec):
        """Imagining four VMPools:
        0. For Linux VMs in private data center (uses OpenVZ)
        1. For Amazon S3 (static content hosting)
        2. For Windows VMs in private data center (uses KVM)
        3. For Amazon EC2
        
        """
        logger.debug("VMPoolManager: get_available_pool()")
        if self.is_lab_static(lab_spec):
            return self.VMPools[1]
        elif self.lab_on_windows(lab_spec):
            return self.VMPools[2]
        else:
            return self.VMPools[0]

    def is_lab_static(self, lab_spec):
        return False

    def lab_on_windows(self, lab_spec):
        return False

    def create_vm(self, lab_spec):
        logger.debug("VMPoolManager: create_vm()")
        vmpool = self.get_available_pool(lab_spec)
        return vmpool.create_vm(lab_spec)

    def undeploy_lab(self, lab_id):
        logger.debug("VMPoolManager: undeploy_lab()")
        used_pools = self.get_used_pools(lab_id)
        for pool_id in used_pools:
            self.VMPools[pool_id].undeploy_lab(lab_id)

    def get_used_pools(self, lab_id):
        logger.debug("VMPoolManager: get_used_pools()")
        return [d['vmpool_info']['vmpool_id'] for d in self.system.state if d['lab_spec']['lab_id']==lab_id]
