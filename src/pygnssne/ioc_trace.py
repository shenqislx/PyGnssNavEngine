"""
IOController Trace Settings
"""
import logging

logger = logging.getLogger(__name__)
file_path = 'debug.log'
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   filename=file_path,
                   filemode='a')


def trace_init():
    with open(file_path, 'w') as file:
        pass
    logger.debug('Logging file cleared!')
