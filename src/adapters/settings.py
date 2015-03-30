OVPL_SRC_DIR = "/../../../ovpl" #above ovpl directory
VM_ROOT_DIR = "/vz/root/"
VM_DEST_DIR = "/root/"
VMMANAGERSERVER_PATH="/root/ovpl/src/VMManager/"
VM_MANAGER_PORT = "9089"

#run VMManagerServer with the default VMManager
VM_MANAGER_SCRIPT = "VMManagerServer.py VMManager"
MAX_VM_ID = 2147483644 # 32-bit; exact value based on trial-and-error

def get_subnet():
    SUBNET = ["10.2.58.128/28"]
    assert isinstance(SUBNET, list)
    return SUBNET

def get_test_lab_id():
    #can be used to create a test lab ID if lab id is empty
    LAB_ID = "engg01"
    assert isinstance(LAB_ID, str)
    assert LAB_ID != ""
    return LAB_ID

def get_test_os():
    #can be used to set a default OS if OS is not specified in lab spec
    OS = "Ubuntu"
    assert isinstance(LAB_ID, str)
    assert OS != ""
    return OS

def get_test_os_version():
    #can be used to set a default OS version if OS is not specified in lab spec
    OS_VERSION = "12.04"
    assert isinstance(OS_VERSION, str)
    assert OS_VERSION != ""
    return OS_VERSION

def get_adapter_nameserver():
    # Required by CentOSVZAdapter.py
    NAME_SERVER = "inherit"
    return NAME_SERVER

def get_adapter_hostname():
    HOST_NAME = "vlabs.ac.in"
    return HOST_NAME
