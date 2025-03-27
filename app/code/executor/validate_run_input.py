import os
import logging
import pandas as pd
from typing import Dict, Any
GIFT_TEMPLATE_PATH = "/computation/gift/GroupICAT/icatb/icatb_templates"

def validate_type(variable, variable_name, expected_types):
    if type(expected_types) != list:
        expected_types = [expected_types]
    if type(variable) not in expected_types:
        raise(TypeError("Got invalid type for variable %s. Expected %s, got %s." % (variable_name, expected_types, type(variable))))
    return

def validate_run_input(in_files: list, data_path: str, local_parameters: Dict[str, Any], log_path: str) -> bool:
    try:

        # Make sure data files exist, and at least one is provided.
        # Currently this shouldn't be a problem because we glob from the 
        # filesystem
        if len(in_files) == 0:
            raise(ValueError("No nifti files were found in data directory."))
        for filename in in_files:
            if not os.path.exists(filename):
                raise(ValueError("Input nifti %s does not exist" % filename))
        # refFiles
        refFiles = local_parameters["refFiles"]
        if not os.path.exists(refFiles) and "neuromark" in refFiles.lower():
            if '.nii' not in refFiles:
                refFiles = refFiles + '.nii'
            refFiles = os.path.join(GIFT_TEMPLATE_PATH, refFiles)
        # Existence
        if not os.path.exists(refFiles):
            raise(ValueError("Input template file %s does not exist on the file system" % refFiles))
        validate_type(refFiles,'refFiles',str)
        # preproc type
        preproc_type = local_parameters["preproc_type"]
        validate_type(preproc_type,'preproc_type',int)
        # scaleType
        scaleType = local_parameters["scaleType"]
        validate_type(scaleType,'scaleType',int)
        # mask
        mask = local_parameters["mask"]
        validate_type(mask,'mask',str)
        if mask not in ['default', 'default&icv']:
            if not os.path.exists(mask):
                raise(ValueError("Mask must be either default, default&icv or a file that exists on the file system. Got %s, which does not exist on the filesystem." % mask))
        # TR
        TR = local_parameters["TR"]
        validate_type(TR,"TR",list)
        # perfType
        perfType = local_parameters["perfType"]
        validate_type(perfType,"perfType",int)
        # dummy_scans
        dummy_scans = local_parameters["dummy_scans"]
        validate_type(dummy_scans,"dummy_scans", list)
        # prefix
        prefix = local_parameters["prefix"]
        validate_type(prefix, "prefix", str)
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
