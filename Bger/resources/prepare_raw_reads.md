
# Extract Reads

Run1:
* 22VCLWLT3_6_R18381_20250131.tar.gz  
* 22VCLWLT3_7_R18381_20250131.tar.gz  
* 22VCLWLT3_8_R18381_20250131.tar.gz

Run2:
* 22WY2VLT3_6_R18589_20250308.tar.gz  
* 22WY2VLT3_7_R18589_20250308.tar.gz  
* 22WY2VLT3_8_R18589_20250308.tar.gz


```bash
nohup tar -xzvf /mnt/data5/sarah/aDNA/sequencing_data/Bger/run1/22VCLWLT3_6_R18381_20250131.tar.gz -C /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set1/ > /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set1/extract_6.log 2>&1 &
nohup tar -xzvf /mnt/data5/sarah/aDNA/sequencing_data/Bger/run1/22VCLWLT3_7_R18381_20250131.tar.gz -C /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set1/ > /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set1/extract_7.log 2>&1 &
nohup tar -xzvf /mnt/data5/sarah/aDNA/sequencing_data/Bger/run1/22VCLWLT3_8_R18381_20250131.tar.gz -C /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set1/ > /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set1/extract_8.log 2>&1 &
nohup tar -xzvf /mnt/data5/sarah/aDNA/sequencing_data/Bger/run2/22WY2VLT3_6_R18589_20250308.tar.gz -C /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set2/ > /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set2/extract_1.log 2>&1 &
nohup tar -xzvf /mnt/data5/sarah/aDNA/sequencing_data/Bger/run2/22WY2VLT3_7_R18589_20250308.tar.gz -C /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set2/ > /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set2/extract_2.log 2>&1 &
nohup tar -xzvf /mnt/data5/sarah/aDNA/sequencing_data/Bger/run2/22WY2VLT3_8_R18589_20250308.tar.gz -C /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set2/ > /mnt/data5/sarah/aDNA/Bger/raw/reads/original/set2/extract_3.log 2>&1 &
```

Check if unzipping is still running:

```bash
ps aux | grep tar.gz
```

# Pre Checking

How to get a list of all relevant `fastq.gz` files. This also includes sub folders

```bash
find . -type f -name "*_R*.fastq.gz"
```

The original data also contains some undetermined reads. to exclude them add `! -iname "*undetermined*"`

```bash
find . -type f -name "*_R*.fastq.gz" ! -iname "*undetermined*"
```

By adding `| wc -l` we can get the number of files

```bash
find . -type f -name "*_R*.fastq.gz" ! -iname "*undetermined*" | wc -l
 ```

# FastQ File Renaming and Moving

## Step 1 - Collect fastq.gz files in Bger/raw/reads

### Script

#### Dry Run
Run this script from Bger/raw/reads. It will consider the sets (set1, set2) in the original folder.
This "dry run" script will not perform any changes, it will only show the user how the moving and renaming would be executed

```bash
#!/bin/bash

count=0

echo "Simulated file moves (only R1/R2, with full path context):"
echo "-----------------------------------------------------------"

for set_dir in original/set*; do
    if [[ -d "$set_dir" ]]; then
        set_name=$(basename "$set_dir")
        for run_dir in "$set_dir"/*; do
            run_id=$(basename "$run_dir")
            demux_dir="$run_dir/demultiplexed"
            if [[ -d "$demux_dir" ]]; then
                for seq_dir in "$demux_dir"/3*/; do
                    seq_id=$(basename "$seq_dir")
                    for fq in "$seq_dir"/*_R[12]_*.fastq.gz; do
                        if [[ -f "$fq" ]]; then
                            ((count++))
                            base_name=$(basename "$fq" .fastq.gz)
                            new_name="${base_name}_${set_name}_${run_id}.fastq.gz"
                            echo "$fq -> ./$(basename "$new_name")"
                        fi
                    done
                done
            fi
        done
    fi
done

echo "-----------------------------------------------------------"
echo "Total R1/R2 .fastq.gz files to be moved: $count"

```

### Real run

```bash
#!/bin/bash

count=0

echo "Moving R1/R2 fastq.gz files and renaming..."

for set_dir in original/set*; do
    if [[ -d "$set_dir" ]]; then
        set_name=$(basename "$set_dir")
        for run_dir in "$set_dir"/*; do
            run_id=$(basename "$run_dir")
            demux_dir="$run_dir/demultiplexed"
            if [[ -d "$demux_dir" ]]; then
                for seq_dir in "$demux_dir"/3*/; do
                    seq_id=$(basename "$seq_dir")
                    for fq in "$seq_dir"/*_R[12]_*.fastq.gz; do
                        if [[ -f "$fq" ]]; then
                            base_name=$(basename "$fq" .fastq.gz)
                            new_name="${base_name}_${set_name}_${run_id}.fastq.gz"
                            # Move and rename file to current directory
                            mv "$fq" "./$new_name"
                            ((count++))
                            echo "Moved: $fq -> ./$new_name"
                        fi
                    done
                done
            fi
        done
    fi
done

echo "-----------------------------------------------------------"
echo "Total files moved: $count"
```

## Purpose
This scripts process sequencing data files organized in the following folder structure:

```
<set>\_#/<sequencing\_run>/demultiplexed/<sequence\_id/>

```

Each `sequence_id` folder contains `.fastq.gz` files (paired-end reads: R1 and R2).

## Objective
- Move all `R1` and `R2` `.fastq.gz` files from their nested folders to the current working directory.
- Rename files to ensure unique filenames by appending:
  - The `set#` folder name
  - The sequencing run folder name
  - The `sequence_id` folder name
- Only move files matching `*_R1_*.fastq.gz` and `*_R2_*.fastq.gz` (exclude `I1` and `I2` index files).

### Example

Original file path:
```
original/set2/22WY2VLT3_8_R18589_20250308/demultiplexed/340272//340272_S44_R1_001.fastq.gz
```

Renamed and moved to current directory as:
```
./340272_S44_R1_001_set2_22WY2VLT3_8_R18589_20250308_340272.fastq.gz
```

### How to Use

1. Run the **dry-run test script** to see what files would be moved and renamed, and count the total files:
2. The dry-run script prints:
   * Source file path
   * New filename it would move to
   * Total count of files matching the criteria
3. Once verified, rund the other script to perform actual moves.

## Step 2 - Renaming the read files for the pipeline

## Objective
For the pipeline we want to perform additional renaming of the files:

1. We want to know the individual and protocol. This can be extracted from the `sequence id`. The relevant values are in the rename file in Google Docs.
2. We want to shorten the filname by
    * replacing the `sequence run` with `lane#` (example `22WY2VLT3_8_R18589_20250308_340272` -> `lane8`)
    * removing `_001`as it is always the same.

This will get us from

```
340272_S44_R1_001_set_2_22WY2VLT3_8_R18589_20250308_340272.fastq.gz
```

to 
```
Bger3_S_340272_S44_R1_set2_lane8.fastq.gz
```

## Renaming files

### Add indiviual and protocol

```bash
python resources/rename.py Bger/resources/rename_step1_runID_to_individual.csv Bger/raw/reads/ --test
```

### Folder to lane

```bash
python resources/rename.py Bger/resources/rename_step2_folder_to_lane.csv Bger/raw/reads/ --test
```

### Remove 001 in name

```bash
python resources/rename.py Bger/resources/rename_step3_remove_001.csv Bger/raw/reads/ --test
```