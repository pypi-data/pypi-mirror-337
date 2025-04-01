import os
import subprocess
import shlex

def FastQC(directory, reads = ["R1"], rerun = False):
    """
    Runs FastQC on trimmed FASTQ files located in the specified directory.

    Parameters:
    - directory (str): Path to the main directory containing the fastp output.
    """
    
    # Create output directory for FastQC if it doesn't exist
    fastqc_output_dir = os.path.join(directory, "FastQC_output")
    
    if not rerun and os.path.isdir(fastqc_output_dir):
        return 0
    
    os.makedirs(fastqc_output_dir, exist_ok=True)
    
    

    for read in reads:

        # Get the list of FASTQ files from the fastp output directory
        fastp_data_dir = os.path.join(directory, f"fastp_output", f"data_{read}")
        fastq_files = [
            file for file in os.listdir(fastp_data_dir) if file.endswith(".fastq") or file.endswith(".fastq.gz")
        ]

        # Run FastQC on each FASTQ file
        for fastq_file in fastq_files:
            fastqc_file = os.path.join(
                fastqc_output_dir, fastq_file.split(".fas")[0] + "_fastqc.html"
            )
            if os.path.isfile(fastqc_file):
                print(f"FastQC file: {fastqc_file} exists!")
            else:
                # Construct and execute the FastQC command
                command = [
                    "fastqc",
                    "-o", fastqc_output_dir,
                    os.path.join(fastp_data_dir, fastq_file)
                ]
                print("Running command:", " ".join(command))
                subprocess.run(command, check=True)


def multiQC(directory, rerun = False):
    """
    Runs MultiQC on the FastQC output files located in the specified directory.

    Parameters:
    - directory (str): Path to the main directory containing the FastQC output.
    """
    fastqc_output_dir = os.path.join(directory, "FastQC_output")
    multiqc_output_dir = os.path.join(directory, "MultiQC_output")

    if not rerun and os.path.isdir(multiqc_output_dir):
        return 0

    # Check if the FastQC output directory exists
    if os.path.isdir(fastqc_output_dir):
        # Construct and execute the MultiQC command
        command = ["multiqc", fastqc_output_dir,
                    "-o", multiqc_output_dir
        ]
        print("Running command:", " ".join(command))
        subprocess.run(command, check=True)
    else:
        print("FastQC output directory not found. Run FastQC(directory) first.")
