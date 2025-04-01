import os
import subprocess
import shlex
import glob

import pandas as pd

def get_basename(filename):
    basename = os.path.basename(os.path.splitext(filename)[0]\
        .split(".fastq")[0]\
            .split("_fastp_output")[0])
    
    return basename

def metadata_upload(directory,
                    meta_delim_whitespace = False,
                    meta_index_col = None):
        
    meta_file_path = os.path.join(directory, "NGS_user_metadata.csv")
    metadata = pd.read_csv(meta_file_path,
                delim_whitespace=meta_delim_whitespace, 
                index_col=meta_index_col)\
                .rename_axis(mapper= None,axis=0)

    metadata["basename"] =  metadata.apply(lambda row:
                        get_basename(row["rawdata_filename"]), axis =1)

    return metadata


def bamCoverage(
    directory, 
    outfileformat="bedgraph", 
    User_inputs_dict=None, 
    strand=None, 
    binSize=20, 
    smoothLength=60, 
    minMappingQuality=255, 
    normalizeUsing=None, 
    staroutDir=None
):
    """
    Run bamCoverage to generate coverage files (e.g., bedgraph, bigwig) from BAM files.

    Parameters:
    - directory (str): Path to the main directory for input and output.
    - outfileformat (str): Format of the output file (e.g., "bedgraph", "bigwig").
    - User_inputs_dict (dict): Dictionary containing user inputs, including transcript filters.
    - strand (str): RNA strand filtering option ("forward" or "reverse").
    - binSize (int): Bin size for coverage calculation (default: 20).
    - smoothLength (int): Smoothing length for coverage calculation (default: 60).
    - minMappingQuality (int): Minimum mapping quality for BAM reads (default: 255).
    - normalizeUsing (str): Normalization method (e.g., "RPKM", "CPM").
    - staroutDir (str): Directory containing STAR output BAM files. Defaults to a subdirectory in `directory`.

    Returns:
    None
    """
    # Handle transcript length filters
    include_transcripts_above = User_inputs_dict.get("include_transcripts_above")
    include_transcripts_below = User_inputs_dict.get("include_transcripts_below")
    
    metadata = metadata_upload(directory)
    metadata_bed =metadata[metadata["BEDGRAPH"]]  
    bedTrue = list(metadata_bed["basename"])

    
    
    # Set input and output file paths
    filter_flag = ""
    input_files = os.path.join(directory, "starout", "*out.bam")
    if include_transcripts_above:
        filter_flag = f"above{include_transcripts_above}"
    elif include_transcripts_below:
        filter_flag = f"below{include_transcripts_below}"

    if filter_flag:
        input_files = os.path.join(directory, "starout", f"*{filter_flag}.bam")
    bam_files = glob.glob(input_files)
    
    bam_files =  [file for file in bam_files if get_basename(file) in bedTrue ]
    
    # Define output directory
    outDir = os.path.join(directory, f"{outfileformat}out")
    os.makedirs(outDir, exist_ok=True)

    # File suffix mappings for output formats
    dict_file_suffix = {
        "bedgraph": ".bedgraph", 
        "bigwig": ".bigwig", 
        "bed": ".bedgraph", 
        "bw": ".bigwig"
    }

    # Strand filtering mappings
    dict_strand = {
        "forward": "rev",  # QuantSeq: forward strand -> rev
        "reverse": "fwd"   # QuantSeq: reverse strand -> fwd
    }

    # Default STAR output directory if not provided
    if not staroutDir:
        staroutDir = os.path.join(directory, "starout")


    # Process each BAM file
    for file in bam_files:
        # Construct base output file path
        outfile = os.path.join(outDir, os.path.basename(file)).replace(".bam", "")
        outfile_w_suffix = outfile + dict_file_suffix[outfileformat]

        # Construct the bamCoverage command
        command = [
            "bamCoverage",
            "-b", os.path.join(staroutDir, file),
            "-o", outfile_w_suffix,
            "-of", outfileformat,
            "--binSize", str(binSize),
            "--minMappingQuality", str(minMappingQuality)
        ]

        # Add strand filtering if specified
        if strand:
            command.extend(["--filterRNAstrand", strand])
            outfile_w_suffix = f"{outfile}_{dict_strand[strand]}{dict_file_suffix[outfileformat]}"

        # Add smoothing length if specified
        if smoothLength:
            command.extend(["--smoothLength", str(smoothLength)])

        # Add normalization if specified
        if normalizeUsing:
            
            normalized_outDir = os.path.join(outDir, f"normalizeUsing{normalizeUsing}")
            os.makedirs(normalized_outDir, exist_ok=True)
            outfile = os.path.join(normalized_outDir, os.path.basename(file)).replace(".bam", "")
            command.extend(["--normalizeUsing", normalizeUsing])
            outfile_w_suffix = f"{outfile}_{normalizeUsing}{dict_file_suffix[outfileformat]}"
            if strand:
                outfile_w_suffix = f"{outfile}_{normalizeUsing}_{strand}{dict_file_suffix[outfileformat]}"

        # Update output file path in the command
        command[4] = outfile_w_suffix

        # Check if the output file already exists
        if os.path.isfile(outfile_w_suffix):
            print(f"File already processed: {outfile_w_suffix}")
        else:
            # Execute the command
            print("Running command:", " ".join(command))
            subprocess.run(command, check=True)
