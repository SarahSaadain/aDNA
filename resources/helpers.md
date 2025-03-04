# aDNA

prepare read list  
```find . -type f \( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \) ! -path "*/undetermined/*" | sort | awk 'NR%2{printf "%s,", $0} NR%2==0{print $0}' > reads_list.txt```  

compare md5sum for 22VCLWLT3_6_R18381_20250131.tar.gz  
```echo "53682ce8865dd90346dd900c5252c6cb" "53682ce8865dd90346dd900c5252c6cb" | awk '{if ($1 == $2) print "Match"; else print "Different"}'```  

compare md5sum for 22VCLWLT3_7_R18381_20250131.tar.gz  
```echo "5c1450be56ae13be60819aace2bd2f43" "5c1450be56ae13be60819aace2bd2f43" | awk '{if ($1 == $2) print "Match"; else print "Different"}'``` 

compare md5sum for 22VCLWLT3_8_R18381_20250131.tar.gz   
```echo "2520eebe030f65eb6f57444514c39f3c" "2520eebe030f65eb6f57444514c39f3c" | awk '{if ($1 == $2) print "Match"; else print "Different"}'```

```bash
grep SUCCESS adapter_remove.log
````

```bash
grep ERROR adapter_remove.log
````

```bash
nohup python -u scripts/pipeline_aDNA.py > pipeline.log 2>&1 &
```

example how to copy the files to the right directory
```bash
for folder in 340134 340146 340154 340155; do
    mv /mnt/data2/sarah/aDNA/batch1_failed_trialrun/$folder /mnt/data2/sarah/aDNA/Sepsis/raw/reads/original/
done
```

then copy the R1 or R2 files to reads directory
```bash
find /mnt/data2/sarah/aDNA/Dsim/raw/reads/original/ -type f \( -name "*R1*.fastq.gz" -o -name "*R2*.fastq.gz" \) -exec mv {} /mnt/data2/sarah/aDNA/Dsim/raw/reads/ \;
```

get ref genomes
```bash
wget --content-disposition "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCF_016746395.2/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=RNA_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=SEQUENCE_REPORT&hydrated=FULLY_HYDRATED"
```
```bash
wget --content-disposition "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_001014415.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=RNA_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=SEQUENCE_REPORT&hydrated=FULLY_HYDRATED"
```