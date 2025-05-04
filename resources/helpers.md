# aDNA

```bash
nohup python -u scripts/pipeline_aDNA.py > pipeline.log 2>&1 &
```

prepare read list  
```bash
find . -type f \( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \) ! -path "*/undetermined/*" | sort | awk 'NR%2{printf "%s,", $0} NR%2==0{print $0}' > reads_list.txt
```  

To move all .fastq.gz files from all subfolders into the current directory, you can use the following command:
```bash
find . -type f -name "*R1_001.fastq.gz" -exec mv {} . \;
```

compare md5sum for 22VCLWLT3_6_R18381_20250131.tar.gz  
```bash
echo "53682ce8865dd90346dd900c5252c6cb" "53682ce8865dd90346dd900c5252c6cb" | awk '{if ($1 == $2) print "Match"; else print "Different"}'  
```

compare md5sum for 22VCLWLT3_7_R18381_20250131.tar.gz  
```bash
echo "5c1450be56ae13be60819aace2bd2f43" "5c1450be56ae13be60819aace2bd2f43" | awk '{if ($1 == $2) print "Match"; else print "Different"}' 
```

compare md5sum for 22VCLWLT3_8_R18381_20250131.tar.gz   
```bash
echo "2520eebe030f65eb6f57444514c39f3c" "2520eebe030f65eb6f57444514c39f3c" | awk '{if ($1 == $2) print "Match"; else print "Different"}'
```

move files by ID to correct folder
Dsim 1trial
```bash
for folder in 340125 340126 340127 340130 340131 340132 340133 340139 340140 340141 340142 340143 340144 340145 340147 340150 340151 340153 340156; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/$folder /mnt/data2/sarah/aDNA/trial_Dsim/
done
```

Dsim 2trial
```bash
for folder in 344209 344210 344211 344214 344215 344216 344217 344223 344224 344225 344226 344227 344228 344229 344231 344234 344235 344237 344240; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/22WY2VLT3_5_R18575_20250308/demultiplexed/$folder /mnt/data2/sarah/aDNA/trial_Dsim/raw/reads/2trial/
done
```

Phortica 1trial
```bash
for folder in 340128 340129 340135 340136 340137 340138 340149; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/$folder /mnt/data2/sarah/aDNA/trial_Phortica/
done
```

Phortica 2trial
```bash
for folder in 344212 344213 344219 344220 344221 344222 344233; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/22WY2VLT3_5_R18575_20250308/demultiplexed/$folder /mnt/data2/sarah/aDNA/trial_Phortica/raw/reads/2trial/
done
```

Sepsis 1trial
```bash
for folder in 340134 340146 340154 340155; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/$folder /mnt/data2/sarah/aDNA/trial_Sepsis/
done
```

Sepsis 2trial
```bash
for folder in 344218 344230 344238 344239; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/22WY2VLT3_5_R18575_20250308/demultiplexed/$folder /mnt/data2/sarah/aDNA/trial_Sepsis/raw/reads/2trial/
done
```

library blanks 2trial
```bash
for folder in 340148 340152; do
    mv /mnt/data2/sarah/aDNA/batch2_failed_trialrun/$folder /mnt/data2/sarah/aDNA/trial_LB/
done
```

then copy the R1 or R2 files to reads directory
```bash
find /mnt/data2/sarah/aDNA/Dsim/raw/reads/original/ -type f \( -name "*R1*.fastq.gz" -o -name "*R2*.fastq.gz" \) -exec mv {} /mnt/data2/sarah/aDNA/Dsim/raw/reads/ \;
```

same thing different code:
```bash
for folder in /mnt/data2/sarah/aDNA/trial_Phortica/raw/reads/2trial/*; do 
    mv "$folder"/*_R[12]_*.fastq.gz /mnt/data2/sarah/aDNA/trial_Phortica/raw/reads/ 
done
```

```bash
grep SUCCESS adapter_remove.log
````

```bash
grep ERROR adapter_remove.log
````



# get ref genomes
```bash
wget --content-disposition "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCF_016746395.2/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=RNA_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=SEQUENCE_REPORT&hydrated=FULLY_HYDRATED"
```
```bash
wget --content-disposition "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_001014415.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=RNA_FASTA&include_annotation_type=CDS_FASTA&include_annotation_type=PROT_FASTA&include_annotation_type=SEQUENCE_REPORT&hydrated=FULLY_HYDRATED"
```

# important notes
reads longer than 150 after adapter removal, filtering and duplicate removal are due to merging of overlapping reads in fastq

# fix Phortica COI gene file
there was an error while using the fasta file for mapping. when converting the sam to bam i got this error:
```
[E::sam_parse1] SEQ and QUAL are of different length 
````

i used below command to add a dummy quality score

```bash
awk 'BEGIN {OFS="\n"} /^>/ {header=$0; getline seq; qual=""; for(i=1;i<=length(seq);i++) qual=qual "I"; print header, seq, "+", qual}' phortica_coi.fna > phortica_coi.fastq
```
