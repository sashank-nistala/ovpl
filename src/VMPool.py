""" 
VMPool manages a pool of VMs and the resources available for use by the VMs.
Resources may include RAM, diskspace, IPs, etc.  For now, these resources 
are handled by the platform adapters.  VMPool does this by maintaining a
list of VMs via corresponding VMProxy objects.

"""

__all__ = [
    'VMProxy',
    'VMPool',
    ]

import json
import requests
from exceptions import Exception
from http_logging.http_logger import logger
from State import State
from adapters.VMUtils import convert_to_megs
from ads_to_dataservices import *
import ads_to_dataservices
#Globals
CREATE_PATH = "/api/1.0/vm/create"
DESTROY_PATH = "/api/1.0/vm/destroy"

labs_id=0

class VMPool:
    """ Manages a pool of VMs or VMProxy's """

    def __init__(self, vmpool_id, vm_description, adapter_ip, adapter_port, create_path, destroy_path):

        logger.debug("VMPool: __init__(); poolID=%s, Desciption=%s, AdapterIP=%s, AdapterPort=%s, CreatePath=%s, DestroyPath=%s" % \
                             (vmpool_id, vm_description, adapter_ip, adapter_port, create_path, destroy_path))        

        self.system = State.Instance()
        #self.vms = []       # List of VMProxy objects
        self.vmpool_id = vmpool_id
        self.vm_description = vm_description
        self.adapter_ip = adapter_ip
        self.adapter_port = adapter_port
        self.create_path = create_path
        self.destroy_path = destroy_path


    def create_vm(self, lab_spec):
        # vm_spec is a json string
        # Allocate a vm_id: not required as platform adapter will allocate it.
        # Invoke platform adapter server (POST)
	#print type(lab_spec)
        def construct_state():
            return {
                "lab_spec": lab_spec,
                "vm_info": {
                    "vm_id": vm_id,
                    "vm_ip": vm_ip,
                    "vmm_port": vmm_port
                },
                "vmpool_info": {
                    "vmpool_id": self.vmpool_id,
                    "vm_description": self.vm_description,
                    "adapter_ip": self.adapter_ip,
                    "adapter_port": self.adapter_port
                },
                "vm_status": {
                    "last_known_status": None,
                    "last_successful_connection": None,
                    "reconnect_attempts": None,
                    "disk_usage": None,
                    "mem_usage": None
                },
                "lab_history": {
                    "released_by": None,
                    "released_on": None,
                    "destroyed_by": None,
                    "destroyed_on": None
                }
            }

        logger.debug("VMPool: create_vm(); poolID=%s, Desciption=%s, AdapterIP=%s, AdapterPort=%s, CreatePath=%s, DestroyPath=%s" % \
                             (self.vmpool_id, self.vm_description, self.adapter_ip, self.adapter_port, self.create_path, self.destroy_path))

        adapter_url = "%s:%s%s" % (self.adapter_ip, self.adapter_port, self.create_path)
        payload = {"lab_spec": json.dumps(lab_spec)}
	
	logger.debug("VMPool: create_vm(); adapter_url = %s, payload = %s" % (adapter_url, str(payload)))

        try:
            result = requests.post(url=adapter_url, data=payload)
            logger.debug("VMPool: create_vm(): Response text from adapter: " + result.text)
            if result.status_code == requests.codes.ok:
                vm_id = result.json()["vm_id"]
                vm_ip = result.json()["vm_ip"]
                vmm_port = result.json()["vmm_port"]
		
	        
		return construct_state()
            else:
                raise Exception("VMPool: create_vm(): Error creating VM: " + result.text)
        except Exception, e:
            logger.error("VMPool: create_vm(): Error communicating with adapter: " + str(e))
            raise Exception("VMPool: create_vm(): Error creating VM: " + str(e))

    def destroy_vm(self, vm_id):
        # Invoke platform adapter
        # Delete entry from VMs list
        logger.debug("VMPool.destroy_vm()")
        adapter_url = "%s:%s%s" % (self.adapter_ip, self.adapter_port, self.destrpy_path)
        payload = {'vm_id': vm_id}
        try:
            result = requests.post(url=adapter_url, data=payload)
            logger.debug("Response text from adapter: " + result.text)
            if result.status_code == requests.codes.ok and "Success" in result.text:
                logger.debug("VMPool.destroy_vm()")
                return True
            else:
                logger.error("Error destroying vm: " + result.text)
        except Exception, e:
            logger.error("Error communicating with adapter: " + str(e))

    def save_state(self, lab_id, vm_id):
        for r in self.system.state:
            if r['lab_spec']['lab_id'] == lab_id and r['vm_info']['vm_id'] == vm_id and r['vmpool_info']['vmpool_id'] == self.vmpool_id:
                self.system.state.remove(r)
                self.system.save()
                break

    def destroy_and_save(self, lab_id, vm_id):
        if self.destroy_vm(vm_id):
            self.save_state(lab_id, vm_id)

    def undeploy_lab(self, lab_id):
        logger.debug("VMPool.undeploy_lab()")
        map(lambda vm_id: self.destroy_and_save(lab_id, vm_id), self.dedicated_vms(lab_id))

    def dedicated_vms(self, lab_id):
        this_lab_vms = set([r['vm_info']['vm_id'] for r in self.system.state if r['lab_spec']['lab_id']==lab_id and r['vmpool_info']['vmpool_id']==self.vmpool_id])
        other_lab_vms = set([r['vm_info']['vm_id'] for r in self.system.state if r['lab_spec']['lab_id']!=lab_id and r['vmpool_info']['vmpool_id']==self.vmpool_id])
        return list(this_lab_vms - other_lab_vms)


if __name__ == "__main__":
    pool = VMPool("http://10.4.12.24", "8000")
    pool.create_vm(None)
