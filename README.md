# aDNA

prepare read list  
```find . -type f \( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \) ! -path "*/undetermined/*" > read_files.txt```  