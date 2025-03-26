import logging
import os
import json
import glob
from nvflare.apis.executor import Executor
from nvflare.apis.shareable import Shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.signal import Signal
from utils.utils import get_data_directory_path, get_output_directory_path
from .perform_scica import gift_gica
from .json_to_html_results import json_to_html_results
from .validate_run_input import validate_run_input

GIFT_TEMPLATE_PATH = "/computation/gift/GroupICAT/icatb/icatb_templates"

# Task names
TASK_NAME_PERFORM_COMPUTATION = "perform_scica"
TASK_NAME_SAVE_AGGREGATE_RESULTS = "save_aggregate_scica_results"

class ScicaExecutor(Executor):
    def __init__(self):
        """
        Initialize the SrrExecutor. This constructor sets up the logger.
        """
        logging.info("ScicaExecutor initialized")
    
    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        """
        Main execution entry point. Routes tasks to specific methods based on the task name.
        
        Parameters:
            task_name: Name of the task to perform.
            shareable: Shareable object containing data for the task.
            fl_ctx: Federated learning context.
            abort_signal: Signal object to handle task abortion.
            
        Returns:
            A Shareable object containing results of the task.
        """
        if task_name == TASK_NAME_PERFORM_COMPUTATION:
            return self._do_task_perform_scica(shareable, fl_ctx, abort_signal)
        elif task_name == TASK_NAME_SAVE_AGGREGATE_RESULTS:
            return self._do_task_save_scica_results(shareable, fl_ctx, abort_signal)
        else:
            # Raise an error if the task name is unknown
            raise ValueError(f"Unknown task name: {task_name}")
        
    def _do_task_perform_scica(
        self,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        """
        Perform spatially constrained ICA on local data.

        Returns:
            A Shareable object with the regression results.
        """
        # Paths to data directories and logs
        data_directory = get_data_directory_path(fl_ctx)
        in_files = list(glob.glob(os.path.join(data_directory, "*.nii*")))
        out_dir = get_output_directory_path(fl_ctx)

        local_parameters_path = os.path.join(data_directory, "parameters.json")
        local_parameters = json.load(open(local_parameters_path, "r"))
        computation_parameters = fl_ctx.get_peer_context().get_prop("COMPUTATION_PARAMETERS")
        log_path = os.path.join(get_output_directory_path(fl_ctx), "validation_log.txt")
        
        # Validate the run inputs (covariates, dependent data, and parameters)
        is_valid = validate_run_input(in_files, data_directory, computation_parameters, log_path)
        #is_valid = True
        if not is_valid:
            # Halt execution if validation fails
            raise ValueError(f"Invalid run input. Check validation log at {log_path}")
        
        # Extract options for cleaner pass to function
        refFiles = local_parameters["refFiles"]
        if not os.path.exists(refFiles) and "neuromark" in refFiles.lower():
            if '.nii' not in refFiles:
                refFiles = refFiles + '.nii'
            refFiles = os.path.join(GIFT_TEMPLATE_PATH, refFiles)
        preproc_type = local_parameters["preproc_type"]
        scaleType = local_parameters["scaleType"]
        mask = local_parameters["mask"]
        TR = local_parameters["TR"]
        perfType = local_parameters["perfType"]
        dummy_scans = local_parameters["dummy_scans"]
        prefix = local_parameters["prefix"]
        
        # Perform GICA using Nipype functions
        result = gift_gica(in_files=in_files, 
                               refFiles=refFiles, 
                               out_dir=out_dir,
                               preproc_type=preproc_type, 
                               scaleType=scaleType,
                               mask=mask,
                               TR=TR,
                               perfType=perfType,
                               dummy_scans=dummy_scans,
                               prefix=prefix)
        

        # Prepare the Shareable object to send the result to other components

        outgoing_shareable = Shareable()
        # For now, there is nothing to send to the aggregator
        # In the future, we may want to send local files to compute a mean map
        # or some other aggregate statistic
        outgoing_shareable["result"] = {}
        return outgoing_shareable

    def _do_task_save_scica_results(
        self,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal
    ) -> Shareable:
        """
        For SCICA this currently does nothing; however, I am leaving this function
        in case we want to implement some kind of aggregation in the near future.

        This method retrieves the global regression results from the Shareable object,
        saves them in JSON and HTML format, and returns a Shareable object.
        """
        # Retrieve the global regression result from the Shareable object
        result = shareable.get("result")
        
        
        
        return Shareable()

