
from http_logging.http_logger import logger
from State import State


class VMProxy:
    """ The proxy object corresponding to a VM """

    def __init__(self, vm_id, ip_address, port):
        self.vm_id = vm_id.strip()
        self.ip_address = ip_address.strip()
        self.port = port.strip()

