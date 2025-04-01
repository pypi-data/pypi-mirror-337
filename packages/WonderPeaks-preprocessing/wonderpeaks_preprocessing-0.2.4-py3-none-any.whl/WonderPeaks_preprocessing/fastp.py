import os
import subprocess
import shlex
import shutil

def Run_fastp(directory, librarykit="QuantSeq", adapter_sequence=None, rerun=False, reads=["R1"]):
    """
    Run FastP to preprocess FASTQ files in a specified directory.

    Parameters:
    - directory (str): Path to the directory containing raw data in a subdirectory called "raw_data".
    - librarykit (str): Library preparation kit, either "QuantSeq" or "Corall" (default: "QuantSeq").
    - adapter_sequence (str): Custom adapter sequence for trimming (default: None).
    - rerun (bool): Whether to rerun processing even if output files already exist (default: False).
    - reads (list): List of read identifiers to process (e.g., ["R1", "R2"]).
    """

    raw_directory = os.path.join(directory, "raw_data")
    for read in reads:
        # Define paths
        raw_data_directory = os.path.join(raw_directory, f"raw_data_{read}")
        fastp_output_directory = os.path.join(directory, "fastp_output")
        fastp_data_directory = os.path.join(fastp_output_directory, f"data_{read}")


        # Create necessary directories if they don't exist
        os.makedirs(fastp_data_directory, exist_ok=True)

        # Identify input FASTQ files
        fastqfiles = [
            os.path.join(raw_data_directory, file) 
            for file in os.listdir(raw_data_directory) 
        ]

        # Process each FASTQ file
        for fastqfile in fastqfiles:
            # Determine file extension
            file_handle = ".fastq.gz" if ".gz" in fastqfile else ".fastq"

            # Construct output file path
            fastpfile_base = os.path.join(fastp_data_directory, os.path.basename(fastqfile).replace(file_handle, ""))
            fastpfile_new_handle = f"{fastpfile_base}_fastp_output{file_handle}"

            # Check if rerun is needed
            if rerun or (not os.path.isfile(fastpfile_new_handle) and "fastp" not in fastqfile):
                # Construct FastP command
                if librarykit == "QuantSeq":
                    command = [
                        "fastp",
                        "-i", fastqfile,
                        "-o", fastpfile_new_handle,
                        "--trim_poly_x",
                        "--thread=20",
                    ]
                elif librarykit == "Corall":
                    command = [
                        "fastp",
                        "-i", fastqfile,
                        "-o", fastpfile_new_handle,
                        "--trim_poly_x",
                        "-U", "--umi_loc=read1", "--umi_len=12",
                        "--thread=20",
                    ]
                else:
                    raise ValueError(f"Unsupported library kit: {librarykit}")

                # Add custom adapter sequence if provided
                if adapter_sequence:
                    command.extend([f"--adapter_sequence={adapter_sequence}"])

                # Print and execute the command
                print("Running command:", " ".join(command))
                command_line = " ".join(command)
                args = shlex.split(command_line)
                subprocess.run(args, check=True)

                # Rename log files to avoid overwriting
                os.rename("fastp.html", f"{fastpfile_base}_fastp.html")
                os.rename("fastp.json", f"{fastpfile_base}_fastp.json")

                #  Organize `.html` and `.json` files into subdirectories
                organize_fastp_logs(fastp_output_directory, fastp_data_directory)

            else:
                print(f"File already processed: {fastpfile_new_handle}")

       

def organize_fastp_logs(fastp_output_directory, fastp_data_directory):
    """
    Moves .html and .json files in the fastp_output directory to separate subdirectories.

    Parameters:
    - fastp_output_directory (str): Path to the main fastp_output directory.
    """
    # Define subdirectories for logs
    html_dir = os.path.join(fastp_output_directory, "html")
    json_dir = os.path.join(fastp_output_directory, "json")

    # Create subdirectories if they don't exist
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    # Move files based on their extensions
    for file in os.listdir(fastp_data_directory):
        file_path = os.path.join(fastp_data_directory, file)
        if file.endswith(".html"):
            shutil.move(file_path, os.path.join(html_dir, file))
            print(f"Moved {file} to {html_dir}")
        elif file.endswith(".json"):
            shutil.move(file_path, os.path.join(json_dir, file))
            print(f"Moved {file} to {json_dir}")