import logging

# Setup logger.
def setup_logger():
    logger = logging.getLogger('global_logger')
    logger.setLevel(logging.INFO)

    # Create a file handler
    handler = logging.FileHandler('global.log')

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# Create logger.
logger = setup_logger()
