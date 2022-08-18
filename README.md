# bamtofastq-latch
A basic utility workflow to extract metrics and reads from BAM files

bamtofastq uses the picard-tools package (and its SamToFastq function) to extract reads 1 and 2 from bam (or sam) files. It will also generate flagstat metrics from the bam file.

### Usage

Bam files can contain single or pair-end reads. Upload from your Latch console and select an output file name. The resulting name will be of format:

```{name}_1.fastq.gz```

Select an output folder to capture the ```fastq``` and ```txt``` files. 

### Arguments

* __bam__: Bam file to take metrics from.
* __name__: Name for output FASTQ files.
* __output_dir__: Latch console destination for output files.
* __paired__: Are BAM files from paired-end reads?

### Dependencies

* [samtools](http://www.htslib.org/)
* [picard-tools](https://broadinstitute.github.io/picard/)
* [LatchBio](https://latch.bio/)