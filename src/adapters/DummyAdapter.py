# Author: Siddharth 
# Contact: siddu.druid@gmail.com

""" A module which is a mock adapter - it pretends to setup VM's and the like but actually does nothing """ 

__all__ = [
    'create_vm',
    'start_vm',
    'stop_vm',
    'restart_vm',
    'start_vm_manager',
    'destroy_vm',
    'is_running_vm',
    'migrate_vm',
    'get_resource_utilization',
    'take_snapshot',
    'InvalidVMIDException',
    ]

# Standard Library imports
import re
import os
import shutil
from exceptions import Exception

# Third party imports
import netaddr
import sh

# VLEAD imports
import BaseAdapter
import VMUtils
from dict2default import dict2default
from settings import *
from utils.git_commands import *
from http_logging.http_logger import logger

# Globals
VZCTL = "/usr/sbin/vzctl"
VZLIST = "/usr/sbin/vzlist -a"
IP_ADDRESS_REGEX = r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}"
#IP_ADDRESS_REGEX = 
# "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";

#list of IP addressses since we cannot expect vz to know cause it's a dummy
IP_ADDRESSES = {}

class InvalidVMIDException(Exception):
    def __init__(msg):
        Exception.__init__(msg)

class DummyAdapter(object):

    def test_logging(self):
        logger.debug("test_logging()")


    def create_vm(self, lab_spec, vm_id=""):
        logger.debug("create_vm()")
        """If no vm_id is specified, it is computed using the last two segments of
           an available IP address; vm_spec is an object """
        #if vm_id == "":
        #    ip_address = find_available_ip()
        #    m = re.match(r'[0-9]+.[0-9]+.([0-9]+).([0-9]+)', ip_address)
        #    if m != None:
        #        vm_id = m.group(1) + m.group(2)
        #else:
        #    ip_address = None
        

        #set the ip address to 127.0.0.1 (loopback)
        ip_address = "127.0.0.1"
        vm_id = 127

        vm_id = validate_vm_id(vm_id)
        (vm_create_args, vm_set_args) = construct_vzctl_args(lab_spec)

        logger.debug("create_vm(): ip = %s, vm_id = %s, vm_create_args = %s, vm_set_args = %s" % \
                              (ip_address, vm_id, vm_create_args, vm_set_args))

        #setup IP ADRESS link so that we can map IP addresses to vm id's later
        IP_ADDRESSES[str(vm_id)] = ip_address

        return vm_id
      

    def restart_vm(self, vm_id):
        vm_id = validate_vm_id(vm_id)
     
        return self.start_vm_manager(vm_id)

    # Function alias
    start_vm = restart_vm

    def init_vm(self, vm_id, lab_repo_name):
        copy_vm_manager_files(vm_id)
        self.start_vm_manager(vm_id)
      
        # Return the VM's IP and port info
        response = {"vm_id": vm_id, "vm_ip": get_vm_ip(vm_id), "vmm_port": VM_MANAGER_PORT}
        success = True
        return (success, response)

    def start_vm_manager(self, vm_id):
        return True

    def get_resource_utilization(self):
        pass

    def stop_vm(self, vm_id):
        vm_id = validate_vm_id(vm_id)

    def destroy_vm(self, vm_id):
        vm_id = validate_vm_id(vm_id)
        return "Success"

    def is_running_vm(self, vm_id):
        vm_id = validate_vm_id(vm_id)
        pass



    def migrate_vm(self, vm_id, destination):
        vm_id = validate_vm_id(vm_id)
        pass

    def take_snapshot(self, vm_id):
        vm_id = validate_vm_id(vm_id)
        pass

def construct_vzctl_args(lab_specz={}):
    """ Returns a tuple of vzctl create arguments and set arguments """

    def get_vm_spec():
        lab_spec = dict2default(lab_specz)
        vm_spec = { "lab_ID" : lab_spec['lab']['description']['id'],
            "os" : lab_spec['lab']['runtime_requirements']['platform']['os'],
            "os_version" : lab_spec['lab']['runtime_requirements']['platform']['osVersion'],
            "ram" : lab_spec['lab']['runtime_requirements']['platform']['memory']['min_required'],
            "diskspace" : lab_spec['lab']['runtime_requirements']['platform']['storage']['min_required'],
            "swap" : lab_spec['lab']['runtime_requirements']['platform']['memory']['swap']
        }
        return vm_spec

    vm_spec = get_vm_spec()
    lab_ID = get_test_lab_id() if vm_spec["lab_ID"] == "" else vm_spec["lab_ID"]
    host_name = lab_ID + "." + get_adapter_hostname()
    ip_address = BaseAdapter.find_available_ip()
    os_template = find_os_template(vm_spec["os"], vm_spec["os_version"])
    (ram, swap) = VMUtils.get_ram_swap(vm_spec["ram"], vm_spec["swap"])
    (disk_soft, disk_hard) = VMUtils.get_disk_space(vm_spec["diskspace"])
    vm_create_args = " --ostemplate " + os_template + \
                     " --ipadd " + ip_address + \
                     " --diskspace " + disk_soft + ":" + disk_hard + \
                     " --hostname " + host_name
    # Note to self: check ram format "0:256M" vs "256M"
    vm_set_args = " --nameserver " + get_adapter_nameserver() + \
                  " --ram " + ram + \
                  " --swap " + swap + \
                  " --onboot yes" + \
                  " --save"
    return (vm_create_args, vm_set_args)



def find_os_template(os, os_version):
    # What to do when request comes for unavailable OS/version?
    os = OS.upper() if os == "" else os.strip().upper()
    os_version = OS_VERSION if os_version == "" else os_version.strip()
    if os == "UBUNTU":
        if os_version == "12.04" or os_version == "12":
            return "ubuntu-12.04-custom-x86_64"
        elif os_version == "11.10" or os_version == "11":
            return "ubuntu-11.10-x86_64"
    elif os == "CENTOS":
        if os_version == "6.3":
            return "centos-6.3-x86_64"
        elif os_version == "6.2":
            return "centos-6.2-x86_64"
    elif os == "DEBIAN":
        if os_version == "6.0" or os_version == "6":
            return "debian-6.0-x86_64"
    else:
        pass

def validate_vm_id(vm_id):
    raw_id = str(vm_id).strip() 

    m = re.match(r'^([0-9]+)$', raw_id)
    if m == None:
        raise InvalidVMIDException("Invalid VM ID.  VM ID must be numeric.")
    raw_id = int(m.group(0))
    if raw_id <= 100:
        raise InvalidVMIDException("Invalid VM ID.  VM ID must be greater than 100.")
    if raw_id > MAX_VM_ID:
        raise InvalidVMIDException("Invalid VM ID.  Specify a smaller VM ID.")
    return str(raw_id)


def copy_vm_manager_files(vm_id):
    logger.debug("copy_vm_manager_files(): vm_id = %s" % vm_id)
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    src_dir = current_file_path + VM_MANAGER_SRC_DIR
    dest_dir = "%s%s%s" % (VM_ROOT_DIR, vm_id, VM_MANAGER_DEST_DIR)
    logger.debug("copy_vm_manager_files(): dest_dir = %s, src_dir = %s" % (dest_dir, src_dir))
      

def get_vm_ip( vm_id):
    vm_id = validate_vm_id(vm_id)
    return IP_ADDRESSES[vm_id]
   

def test():
    #vm_spec = VMSpec.VMSpec({'lab_ID': 'test99'})
    import json
    lab_spec = json.loads(open("sample_lab_spec.json").read())
    create_vm(lab_spec)
    create_vm(lab_spec, "99100")
    #create_vm(vm_spec, "99101")
    #create_vm("99102", vm_spec)
    #create_vm("99103", vm_spec)
    destroy_vm("99100")
    #destroy_vm("99101")
    #destroy_vm("99102")
    #destroy_vm("99103")    


if __name__ == "__main__":
    # Start an HTTP server and wait for invocation
    # Parse the invocation command and route to 
    # appropriate methods.
    test()
