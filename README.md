# aDNA

prepare read list  
```find . -type f \( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \) ! -path "*/undetermined/*" | sort | awk 'NR%2{printf "%s,", $0} NR%2==0{print $0}' > reads_list.txt```  