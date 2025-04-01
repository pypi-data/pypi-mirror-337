import os
import subprocess
import shlex
import pandas as pd  # Assuming this is required for the DataFrame operations
import math

class STAR:
    def __init__(
        self, directory, User_inputs_dict, 
        ):
        """
        Initialize the STAR object with alignment parameters.

        Parameters:
        - directory (str): The base directory for RNAseq data.
        - User_inputs_dict (dict): dictionary created from uploaded csv
        - include_transcripts_above (int): Exclude transcripts shorter than this length.
        - include_transcripts_below (int): Exclude transcripts longer than this length.
        """
        self.directory = directory
        self.inputs = User_inputs_dict
        self.include_transcripts_above = self.inputs["include_transcripts_above"]
        self.include_transcripts_below = self.inputs["include_transcripts_below"]
        self.reads = self.inputs["reads"]


        # Validate transcript length filters
        
        if math.isnan(float(self.include_transcripts_above)) and math.isnan(float(self.include_transcripts_below)):
            raise ValueError("Cannot exclude transcripts both above and below specified lengths.")

    def STAR_genome_index(self):
        """
        Generate a genome index using STAR if it doesn't already exist.
        """
        Dir, fasta, GTF = os.path.join(self.directory, "STAR_genome_directory"), self.inputs["genome_fasta_path"], self.inputs["genome_annotations_path"]
        
        
        # this command will create a new genome direcory called "STAR_genome_directory"
        command = [
            "STAR", "--runThreadN", "5",
            "--runMode", "genomeGenerate",
            "--genomeDir", Dir,
            "--genomeFastaFiles", fasta,
            "--sjdbGTFfile", GTF,
            "--sjdbOverhang", "62",
            "--genomeSAindexNbases", "10"
        ]

        if os.path.isdir(Dir):
            print(f"Star genome directory already created: ", Dir)
            return 0
        else:
            print("Running command:", " ".join(command))
            subprocess.run(command, check=True)

    def indexBAM(self, file):
        """
        Index a BAM file using samtools.

        Parameters:
        - file (str): The BAM file to index.
        """
        bam_file = os.path.join(self.directory, "starout", file)
        bai_file = bam_file + ".bai"

        if not os.path.isfile(bai_file):
            command = ["samtools", "index", bam_file]
            print("Running command:", " ".join(command))
            subprocess.run(command, check=True)
                
        else:
            print(f"Index file already processed: {bai_file}")
        

    def filterBAM(self):
        """
        Filter BAM files based on transcript length criteria.
        """
        starout_dir = os.path.join(self.directory, "starout")
        for file in [f for f in os.listdir(starout_dir) if f.endswith("out.bam") and not f.endswith("out.bam.bai")]:
            if self.include_transcripts_above:
                filterlength = f"length(seq)>{self.include_transcripts_above}"
                filter_file = file.replace(".bam", f"_above{self.include_transcripts_above}.bam")
            elif self.include_transcripts_below:
                filterlength = f"length(seq)<{self.include_transcripts_below}"
                filter_file = file.replace(".bam", f"_below{self.include_transcripts_below}.bam")
            else:
                continue

            filter_command = ["--expr", f"{filterlength}"]
            filter_file_path = os.path.join(starout_dir, filter_file)
            filter_bai_file_path = filter_file_path + "bai"

            if not os.path.isfile(filter_file_path):
                command = [
                    "samtools", "view",
                    "-O", "BAM",
                    "-o", filter_file_path,
                    os.path.join(starout_dir, file)
                ] + filter_command
                print("Running command:", " ".join(command))
                subprocess.run(command, check=True)
                
            else:
                print(f"Filtered file already processed: {filter_file_path}")

            if not os.path.isfile(filter_bai_file_path):
                self.indexBAM(filter_file)
                


    def runSTAR_alignment(self, command, out_prefix):
        print("Running command:", " ".join(command))
        subprocess.run(command, check=True)

        bam_file = f"{out_prefix}Aligned.sortedByCoord.out.bam"
        bai_file = f"{out_prefix}Aligned.sortedByCoord.out.bam.bai"
        
        if not os.path.isfile(bai_file):
            self.indexBAM(bam_file)
        
    
    def STAR_alignment(self, rerun=False):
        """
        Align reads using STAR.

        Parameters:
        - rerun (bool): Whether to re-run alignment if output files already exist.
        """
        self.STAR_genome_index()  # Ensure genome index is initialized
        starout_dir = os.path.join(self.directory, "starout")
        os.makedirs(starout_dir, exist_ok=True)

        for read in self.reads:
            fastp_data_dir = os.path.join(self.directory, f"fastp_output", f"data_{read}")
            for file in [f for f in os.listdir(fastp_data_dir) if f.endswith(".fastq") or f.endswith(".fastq.gz")]:
                filepath = os.path.join(fastp_data_dir, file)
                out_prefix = os.path.join(starout_dir, file) + "_"
                bam_file = f"{out_prefix}Aligned.sortedByCoord.out.bam"
                
                command = [
                    "STAR",
                    "--genomeDir", os.path.join(self.directory, "STAR_genome_directory"),
                    "--runMode", "alignReads",
                    "--readFilesIn", filepath,
                    "--runThreadN", "20",
                    "--outSAMtype", "BAM", "SortedByCoordinate",
                    "--outReadsUnmapped", "Fastx",
                    "--outFileNamePrefix", out_prefix,
                    "--limitBAMsortRAM", "31000000000",
                    "--outSAMmultNmax", "10",
                    "--alignIntronMax", "1000",
                    "--alignIntronMin", "4"
                ]
                
                if file.endswith(".gz"):
                    command.extend(["--readFilesCommand", "gunzip", "-c"])
                
                if os.path.isfile(bam_file) and not os.path.isfile(f"{out_prefix}Log.final.out"):
                    # patch to resolve interrupt error
                    print(f"STAR Alignment will rerun alignment on: {filepath}")
                    self.runSTAR_alignment(command, out_prefix)
                    
                if os.path.isfile(bam_file) and not rerun:
                    print(f"Alignment file already processed: {bam_file}")
                    continue
                
                self.runSTAR_alignment(command, out_prefix)
                
            if self.include_transcripts_above or self.include_transcripts_below:
                self.filterBAM()