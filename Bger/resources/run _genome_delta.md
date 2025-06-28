# Running GenomeDelta

https://github.com/rpianezza/GenomeDelta

```bash
conda activate GenomeDelta
```

Commands without nohup:
```bash
bash /mnt/data5/sarah/GenomeDelta/linux/main.sh \
  --fq /mnt/data5/sarah/aDNA/Bger/processed/prepared_for_ref_genome/Bger_combined.fastq.gz \
  --fa /mnt/data5/sarah/aDNA/Bger/raw/ref_genome/GCA_000762945.2_Bger_2.0_genomic.fna \
  --of /mnt/data5/sarah/GenomeDelta_runBgerRef \
  --t 15

bash /mnt/data5/sarah/GenomeDelta/linux/main.sh \
  --fq /mnt/data5/sarah/aDNA/Bger/processed/prepared_for_ref_genome/Bger_combined.fastq.gz \
  --fa /mnt/data5/sarah/aDNA/Bger/raw/ref_genome/Bgerracon1.fasta \
  --of /mnt/data5/sarah/GenomeDelta_runBgerracon1 \
  --t 15
```

```bash
nohup bash /mnt/data5/sarah/GenomeDelta/linux/main.sh \
  --fq /mnt/data5/sarah/aDNA/Bger/processed/prepared_for_ref_genome/Bger_combined.fastq.gz \
  --fa /mnt/data5/sarah/aDNA/Bger/raw/ref_genome/GCA_000762945.2_Bger_2.0_genomic.fna \
  --of /mnt/data5/sarah/GenomeDelta_runBgerRef \
  --t 15 > /mnt/data5/sarah/GenomeDelta_runBgerRef/run_BgerRef.out 2>&1 &
```

2025-06-06 -> [1] 3286666

```bash
nohup bash /mnt/data5/sarah/GenomeDelta/linux/main.sh \
  --fq /mnt/data5/sarah/aDNA/Bger/processed/prepared_for_ref_genome/Bger_combined.fastq.gz \
  --fa /mnt/data5/sarah/aDNA/Bger/raw/ref_genome/Bgerracon1.fasta \
  --of /mnt/data5/sarah/GenomeDelta_runBgerracon1 \
  --t 15 > /mnt/data5/sarah/GenomeDelta_runBgerracon1/run_Bgerracon1.out 2>&1 &
```

2025-06-06 -> [2] 3286682