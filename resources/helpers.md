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