import unittest
import os
import sys
import json

tests_spec = json.loads(open("config_for_tests.json").read())
client_logging_module = tests_spec["CLIENT_LOGGING_PATH"]
sys.path.append(client_logging_module)
import Logging

num_logs = tests_spec["NUMBER_OF_LOGS"]
message = tests_spec["LOG_MESSAGE"]
logger_name = tests_spec["LOGGER_NAME"]
level = tests_spec["LOGGING_LEVEL"]
controller_path = tests_spec["CONTROLLER_PATH"]
vmmanager_path = tests_spec["VMMANAGER_PATH"]
adapter_path = tests_spec["ADAPTER_PATH"]


class TestLoggingServer(unittest.TestCase):

    def test_get_logger_returns_logger(self):
        """Test if get_logger() returns logger object"""
        logger = Logging.get_logger(logger_name, level)
        self.assertEquals(logger.__class__.__name__, 'Logger')

    def test_log_using_logger(self):
        """Test if the logging calls write messages to the log files"""
        logger = Logging.get_logger(logger_name, level)
        open(controller_path,  'w').close()
        for i in range(num_logs):
            logger.debug(message)
        self.assertEquals(count_num_lines(controller_path), num_logs)

    def test_multiple_loggers_same_name(self):
        """Test if multiple loggers with same name work"""
        logger1 = Logging.get_logger("controller", level)
        logger2 = Logging.get_logger("controller", level)
        logger3 = Logging.get_logger("controller", level)
        open(controller_path,  'w').close()
        for i in range(num_logs):
            logger1.debug(message)
            logger2.debug(message)
            logger3.debug(message)
        self.assertEquals(count_num_lines(controller_path), num_logs*3)

    def test_multiple_logger_different_names(self):
        """Test if multiple loggers with different name work"""
        logger1 = Logging.get_logger("controller", level)
        logger2 = Logging.get_logger("vmmanager", level)
        logger3 = Logging.get_logger("adapter", level)
        open(controller_path,  'w').close()
        open(vmmanager_path,  'w').close()
        open(adapter_path,  'w').close()
        for i in range(num_logs):
            logger1.debug(message)
            logger2.debug(message)
            logger3.debug(message)
        sum = count_num_lines(controller_path)+count_num_lines(vmmanager_path)\
            + count_num_lines(adapter_path)
        self.assertEquals(sum, num_logs*3)


def count_num_lines(file_name):
    """Returns the count of number of lines in the file"""
    with open(file_name) as f:
        for i,  l in enumerate(f):
            pass
    try:
        return i+1
    except:
        return 0

if __name__ == '__main__':
    unittest.main()
