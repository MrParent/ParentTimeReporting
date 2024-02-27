import logging

# Create a logger
logger = logging.getLogger('global_logger')
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('global.log')

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)