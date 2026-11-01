import logging
import os

from app.core.config import load_config

def setup_logging():
    config = load_config()

    log_directory = config["log_directory"]
    log_file_name = config["log_file_name"]
    log_level = config["log_level"]

    # Create the log directory if it does not exist
    os.makedirs(log_directory, exist_ok=True)

    log_file_path = os.path.join(log_directory,log_file_name)

    # Write logs both to the file and to the console
    file_handler = logging.FileHandler(log_file_path)
    console_handler = logging.StreamHandler()

    logging.basicConfig(
        level = log_level,
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers = [
            file_handler,
            console_handler,
        ],
        force = True
    )


    # Uvicorn also uses logging handler

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()
    uvicorn_logger.propogate = True

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.handlers.clear()
    uvicorn_error_logger.propagate = True

    uvicorn_access_logger = logging.getLogger("uvicorn.error")
    uvicorn_access_logger.handlers.clear()
    uvicorn_access_logger.propagate = True
