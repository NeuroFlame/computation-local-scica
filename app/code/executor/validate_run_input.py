import os
import logging
import pandas as pd
from typing import Dict, Any

def validate_run_input(in_files: list, data_path: str, computation_parameters: Dict[str, Any], log_path: str) -> bool:
    try:

        # Make sure data files exist.
        # Currently this shouldn't be a problem because we glob from the 
        # filesystem
        if len(in_files) == 0:
            raise(ValueError("No nifti files were found in data directory."))
        for filename in in_files:
            if not os.path.exists(filename):
                raise(ValueError("Input nifti %s does not exist" % filename))

        # If all checks pass
        return True

    except Exception as e:
        error_message = f"An error occurred during validation: {str(e)}"
        _log_validation_error(error_message, log_path)
        return False


def _log_validation_error(message: str, log_path: str) -> None:
    """
    Log the validation error message to the console and write it to validation_log.txt.
    """
    logging.error(message)
    try:
        with open(log_path, 'a') as f:
            f.write(f"{message}\n")
            f.flush()  # Ensure data is written to the file
    except IOError as e:
        logging.error(f"Failed to write to log file {log_path}: {e}")
