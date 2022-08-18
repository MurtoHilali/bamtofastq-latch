"""
Extract and rename FASTQs from bam files
"""
import subprocess
from pathlib import Path

from latch import workflow, small_task
from latch.types import LatchFile, LatchDir

@small_task
def backextract(bam: LatchFile, name: str, output_dir: LatchDir, paired: bool = True) -> (LatchDir):

    # A reference to our output fastqs, currently hardcoded
    local_dir = Path("/root/fastqs/").resolve()

    f1 = Path(f"{name}_1.fastq.gz").resolve()
    f2 = Path(f"{name}_2.fastq.gz").resolve()

    _mkdir_cmd = [
        "mkdir",
        "fastqs"
    ]

    _mv_cmd = [
        "mv",
        str(f1),
        str(local_dir)
    ]

    _b2f_cmd = [
        "PicardCommandLine",
        "SamToFastq",
        f"INPUT={str(bam.local_path)}",
        f"FASTQ={str(f1)}"
    ]

    if paired:
        _mv_cmd.insert(2, str(f2))
        _b2f_cmd.append(f"F2={str(f2)}")

    subprocess.run(_mkdir_cmd)
    subprocess.run(_b2f_cmd)
    subprocess.run(_mv_cmd)

    return LatchDir(str(local_dir), output_dir.remote_path)

@small_task
def flagstats(bam: LatchFile, output_dir: LatchDir) -> LatchFile:

    ## generate a txt file containing flagstats

    flagstats = Path("flagstat.txt").resolve()
    
    _flagstats_cmd = [
        "samtools",
        "flagstat",
        str(bam.local_path) 
    ]

    with open(flagstats, "w") as f:
        subprocess.call(_flagstats_cmd, stdout=f)

    return LatchFile(str(flagstats), f"{output_dir.remote_path}/flagstats.txt")

@workflow
def BamToFastq(bam: LatchFile, output_dir: LatchDir, name: str = "read", paired: bool = True):
    """Get reads 1, 2, and metrics from your BAM file.

    bamtofastq
    ----

    bamtofastq uses the picard-tools package (and its SamToFastq function)
    to extract reads 1 and 2 from bam (or sam) files. It will also generate
    flagstat metrics from the bam file.

    ### Usage

    Bam files can contain single or pair-end reads. Upload from your Latch
    console and select an output file name. The resulting name will be of format:

    ```{name}_1.fastq.gz```

    Select an output folder to capture the ```fastq``` and ```txt``` files. 

    __metadata__:
        display_name: bamtofastq
        author:
            name: Murto Hilali
            email: hilali.murto@gmail.com
            github: https://github.com/MurtoHilali
        repository: https://github.com/MurtoHilali/bamtofastq-latch
        license:
            id: MIT

    Args:

        bam:
          Bam file to take metrics from.

          __metadata__:
            display_name: BAM File

        name:
          Name for output FASTQ files.

          __metadata__:
            display_name: Name
        
        output_dir:
          Destination for output files.

          __metadata__:
            display_name: Output Directory

        paired:
          Are BAM files from paired-end reads?

          __metadata__:
            display_name: Paired


    """

    flagstats(bam=bam, output_dir=output_dir)
    return backextract(bam=bam, name=name, output_dir=output_dir, paired=paired)