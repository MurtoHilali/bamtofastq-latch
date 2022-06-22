"""
Extract and rename FASTQs from bam files
"""
import subprocess
from pathlib import Path
# import re, difflib, ast, os

from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def backextract(bam: LatchFile, name: str) -> (LatchFile, LatchFile):

    # A reference to our output.
    
    f1 = Path(f"{name}_1.fastq.gz").resolve()
    f2 = Path(f"{name}_2.fastq.gz").resolve()

    _b2f_cmd = [
        "PicardCommandLine",
        "SamToFastq",
        f"INPUT={str(bam.local_path)}",
        f"FASTQ={str(f1)}",
        f"F2={str(f2)}"
    ]

    ## are bam files usually from paired-end sample?
    ## in which domains/industries/are they single/paired-end?

    subprocess.run(_b2f_cmd)
    
    return (
        LatchFile(str(f1), f"latch:///b2f_outputs/{name}_1.fastq.gz"),
        LatchFile(str(f2), f"latch:///b2f_outputs/{name}_2.fastq.gz")
    )    

@small_task
def flagstats(bam: LatchFile) -> LatchFile:

    flagstats = Path("flagstat.txt").resolve()
    
    _flagstats_cmd = [
        "samtools",
        "flagstat",
        str(bam.local_path) 
    ]
    #
    ## forgot to add the .local_path in an earlier v, 
    ## maybe a womtool validate thing would be good
    with open(flagstats, "w") as f:
        subprocess.call(_flagstats_cmd, stdout=f)

    return LatchFile(str(flagstats), "latch:///b2f_outputs/flagstats.txt")

@workflow
def BamToFastq(bam: LatchFile, name: str = "read") -> (LatchFile, LatchFile):
    """Get reads 1, 2, and metrics from your BAM file.

    bamtofastq
    ----

    bamtofastq uses the picard-tools package (and its SamToFastq function)
    to extract reads 1 and 2 from bam (or sam) files. It will also generate
    flagstat metrics from the bam file.

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
    """

    flagstats(bam=bam)
    return backextract(bam=bam, name=name)

## keep getting a 'successfully registered, even if not'