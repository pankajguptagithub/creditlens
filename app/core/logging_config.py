import logging
import os

from app.core.config import load_config

def setup_logging():
    config = load_config()

    log_directory = config["log_directory"]
    log_file_name = config["log_file_name"]
    log_level = config["log_level"]

    #Create the log directory if it does not exist
    os.makedirs(log_directory, exist_ok=True)

    log_file_path = os.path.join(log_directory,log_file_name)

    logging.basicConfig(
        filename = log_file_path,
        level = log_level,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s" 
    )
