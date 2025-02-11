# Run FASTX-toolkit
```bash
fastq_quality_filter
-q 30 # Minimum quality score to keep.
-p 75 # Minimum percent of bases that must have [-q] quality.
-i input.fastq
-o filtered.fastq
```

# Run SGA https://github.com/jts/sga/blob/master/src/README
removes low-complexity sequences from reads

sga preprocess --dust-threshold=1 --pe-mode 1 -o pair_preprocessed.fastq R1_trimmed.fastq R2_trimmed.fastq

# uses Rope BWT algorithm to index reads
allows for efficient mapping or searching of these sequences later

```bash
sga index -a ropebwt -t 4 preprocessed.fastq 
```

# filters redundant reads (but not with k-mer redundancy)
# meaning it will remove exact duplicates based solely on the full sequende, rather than checking for common k-mer patterns between reads
```bash
sga filter --no-kmer-check preprocessed.fastq > final_filtered.fastq
```

# Run FASTX-toolkit (only in Genome publication)
```bash
fastx_trimmer
-l 20 # Trims reads to a length of 20 bp (do I need that after I trimmed with cutadapt everything below 15bp?)
-i filtered.fastq
-o trimmed.fastq
```