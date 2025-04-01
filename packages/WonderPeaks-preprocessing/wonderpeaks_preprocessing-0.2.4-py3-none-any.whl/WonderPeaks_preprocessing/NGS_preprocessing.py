# import os
# import shutil
# from user_inputs import *
# from fastp import *
# from split_directories import *
# from QC import *
# from STAR_alignment import *
# from bamCoverage import *
# from feature_counts import *
# import pandas as pd
# import csv

"""This function does not work for some reason..."""
# for library in ["quant", "total"]:
#     print(f"Processing {library}")
#     directory = f"/data/Megan/NGS_processing/Example_RNAseq_{library}"
#     User_inputs_dict = initiate_user_inputs(directory)
#     split_files_by_suffix(directory, reads = User_inputs_dict["reads"] )

#     Run_fastp(directory, librarykit= User_inputs_dict["librarykit"], 
#         adapter_sequence=User_inputs_dict["adapter_sequence"], 
#         rerun=False, 
#         reads = User_inputs_dict['reads']
#         )


#     FastQC(directory, reads = User_inputs_dict["reads"], rerun=False)
#     multiQC(directory, rerun=False)
#     STAR(directory, User_inputs_dict, 
#         ).STAR_alignment()


    # # For quantseq, run bamCoverage for PeakStream usage
    # for strand in ["forward", "reverse"]:
    #     bamCoverage(
    #         directory, 
    #         outfileformat="bedgraph", 
    #         User_inputs_dict=User_inputs_dict, 
    #         strand=strand, 
    #         binSize=20, 
    #         smoothLength=None, 
    #         minMappingQuality=255, 
    #         normalizeUsing=None, 
    #         staroutDir=None
    #     )

