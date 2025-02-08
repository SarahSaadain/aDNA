# aDNA

prepare read list  
```find . -type f \( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \) ! -path "*/undetermined/*" | sort | awk 'NR%2{printf "%s,", $0} NR%2==0{print $0}' > reads_list.txt```  

compare md5sum  
```echo "53682ce8865dd90346dd900c5252c6cb" "53682ce8865dd90346dd900c5252c6cb" | awk '{if ($1 == $2) print "Match"; else print "Different"}'``` 