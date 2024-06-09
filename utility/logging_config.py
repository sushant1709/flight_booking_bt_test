import os
import logging

log_directory = os.path.join(os.path.dirname(__file__), '..', 'Logging')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logger = logging.getLogger('RestfulBookerLogger')
logger.setLevel(logging.INFO)

log_file = os.path.join(log_directory, '_booker.log')
fh = logging.FileHandler(log_file, mode='w')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def get_logger(name):
    return logging.getLogger('RestfulBookerLogger').getChild(name)
