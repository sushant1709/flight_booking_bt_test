import os
import logging

# Create Logging directory if it doesn't exist
log_directory = os.path.join(os.path.dirname(__file__), '..', 'Logging')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logger = logging.getLogger('RestfulBookerLogger')
logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages
log_file = os.path.join(log_directory, '_booker.log')
fh = logging.FileHandler(log_file, mode='w')
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def get_logger(name):
    return logging.getLogger('RestfulBookerLogger').getChild(name)
