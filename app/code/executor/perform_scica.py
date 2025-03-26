import os
from nipype.interfaces import gift
import logging

# GICA DEFAULTS
DEFAULT_DIM = 100
DEFAULT_ALG = 16
DEFAULT_ICA_PARAM_FILE = ''
DEFAULT_OUT_DIR = '.'
DEFAULT_DISPLAY_RESULTS = {
    'formatName':'html'
}
DEFAULT_REFS = []
DEFAULT_RUN_NAME = 'COINSTAC_SCICA'
DEFAULT_GROUP_PCA_TYPE = 0
DEFAULT_BACK_RECON_TYPE = 5
DEFAULT_PREPROC_TYPE = 1
DEFAULT_NUM_REDUCTION_STEPS = 1
DEFAULT_SCALE_TYPE = 0
DEFAULT_GROUP_ICA_TYPE = 'spatial'
DEFAULT_WHICH_ANALYSIS = 1
DEFAULT_MASK = ''
DEFAULT_TR = [2]
DEFAULT_DF= 20
DEFAULT_PERFTYPE = 1
DEFAULT_DUMMY_SCANS = [0]
DEFAULT_PREFIX = "gica_cmd"
DEFAULT_PCATYPE = "Standard"
DEFAULT_DO_ESTIMATION = 1
DEFAULT_NUM_WORKERS = 1
DEFAULT_DISPLAY_RESULT_OPTS = {}
DEFAULT_NETWORK_SUMMARY_OPTS = {'comp_network_names':{
"SC": [1, 2, 3, 4, 5],
"AU":[6, 7],
"SM":[8, 9, 10, 11, 12, 13, 14, 15, 16],
"VI":[17, 18, 19, 20, 21, 22, 23, 24, 25],
"CC":[26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
"DM":[43, 44, 45, 46, 47, 48, 49],
"CB":[50, 51, 52, 53]
}}
DEFAULT_ICASSO_OPTS = {}
DEFAULT_MST_OPTS = {}
DEFAULT_DESIGN_MATRIX = []
DEFAULT_REGRESSORS = []

matlab_cmd = '/computation/GroupICATv4.0b_standalone_sep_10_2019/run_groupica.sh /usr/local/MATLAB/MATLAB_Runtime/R2022b/'


def gift_gica(
    in_files=[], 
    dim=DEFAULT_DIM, 
    algoType=DEFAULT_ALG, 
    refFiles=DEFAULT_REFS,
    out_dir=DEFAULT_OUT_DIR, 
    backReconType=DEFAULT_BACK_RECON_TYPE, 
    preproc_type=DEFAULT_PREPROC_TYPE,
    numReductionSteps=DEFAULT_NUM_REDUCTION_STEPS, 
    scaleType=DEFAULT_SCALE_TYPE,
    group_ica_type=DEFAULT_GROUP_ICA_TYPE, 
    display_results=DEFAULT_DISPLAY_RESULTS,
    which_analysis=DEFAULT_WHICH_ANALYSIS, 
    mask=DEFAULT_MASK, 
    TR=DEFAULT_TR, 
    perfType=DEFAULT_PERFTYPE,
    dummy_scans=DEFAULT_DUMMY_SCANS,
    prefix=DEFAULT_PREFIX,
    num_workers=DEFAULT_NUM_WORKERS,
    doEstimation=DEFAULT_DO_ESTIMATION, 
    df=DEFAULT_DF, # unused in scica
    group_pca_type=DEFAULT_GROUP_PCA_TYPE, # unused in scica
    pcaType=DEFAULT_PCATYPE, # unused in scica
    # TODO: finish these options
    display_result_opts=DEFAULT_DISPLAY_RESULT_OPTS, network_summary_opts=DEFAULT_NETWORK_SUMMARY_OPTS,
    icasso_opts=DEFAULT_ICASSO_OPTS, mst_opts = DEFAULT_MST_OPTS, design_matrix = DEFAULT_DESIGN_MATRIX,
    regressors = DEFAULT_REGRESSORS
):
    """
    Wrapper for initializing GIFT nipype interface to run Group ICA.

    Args:
        in_files            (List [Str])    :   Input file names (either single file name or a list)
        dim                 (Int)           :   Dimensionality reduction into #num dimensions
        algoType            (Int)           :   options are 1 - Infomax, 2 - Fast ica , ...
        refFiles            (List [Str])    :   file names for reference templates (either single file name or a list)
        run_name            (Str)           :   Name of the analysis run
        out_dir             (Str)           :   Full file path of the results directory
        group_pca_type      (Str)           :   options are 'subject specific' and 'grand mean'
        backReconType       (Int)           :   options are 1 - regular, 2 - spatial-temporal regression, 3 - gica3, 4 - gica, 5 - gig-ica
        preproc_type        (Int)           :   options are 1 - remove mean per timepoint, 2 - remove mean per voxel, 3 - intensity norm, 4 - variance norm
        numReductionSteps   (Int)           :   Number of reduction steps used in the first pca step
        scaleType           (Int)           :   options are 0 - No scaling, 1 - percent signal change, 2 - Z-scores
        group_ica_type      (Str)           :   1 - Spatial ica, 2 - Temporal ica.
        display_results     (Int)           :   0 - No display, 1 - HTML report, 2 - PDF
        which_analysis      (Int)           :   Options are 1, 2, and 3. 1 - standard group ica, 2 - ICASSO and 3 - MST.
        mask                (Str)           :   Enter file names using full path of the mask. If you wish to use default mask leave it empty

        algoType full options:
        1           2           3       4           5       6
        'Infomax'   'Fast ICA'  'Erica' 'Simbec'    'Evd'   'Jade Opac',
        7           8           9                   10 
        'Amuse'     'SDD ICA'   'Semi-blind'        'Constrained ICA (Spatial)' 
        11              12      13          14      15          16          17
        'Radical ICA'   'Combi' 'ICA-EBM'   'ERBM'  'IVA-GL'    'GIG-ICA'   'IVA-L'

    Args (not supported here, but available for nipype):
        perfType            (Int)           :   Options are 1, 2, and 3. 1 - maximize performance, 2 - less memory usage  and 3 - user specified settings.
        prefix              (Str)           :   Enter prefix to be appended with the output files
        dummy_scans         (Int)           :   enter dummy scans
        numWorkers          (Int)           :   Number of parallel workers    
        doEstimation        (Int)           :   options are 0 and 1 


    """
    gift.GICACommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)

    gc = gift.GICACommand()
    gc.inputs.in_files = in_files
    gc.inputs.algoType = algoType
    gc.inputs.backReconType = backReconType
    gc.inputs.preproc_type = preproc_type
    gc.inputs.numReductionSteps = numReductionSteps
    gc.inputs.scaleType = scaleType
    gc.inputs.group_ica_type = group_ica_type
    gc.inputs.which_analysis = which_analysis
    gc.inputs.refFiles = refFiles
    gc.inputs.display_results = display_results
    gc.inputs.mask = mask
    gc.inputs.TR = TR
    gc.inputs.prefix = prefix
    gc.inputs.dummy_scans = dummy_scans
    gc.inputs.perfType = perfType

    if dim > 0:
        gc.inputs.dim = dim

    gc.inputs.out_dir = out_dir
    output = {}
    
    output = gc.run()
    
    
    return output