nohup bash /mnt/data2/philipp/GenomeDelta/linux/main.sh --fq /mnt/data2/sarah/aDNA/Bger/processed/genome_delta/Bger_combined_all_reads.fastq.gz --fa /mnt/data2/sarah/aDNA/Bger/raw/ref_genome/GCA_000762945.2_Bger_2.0_genomic.fna  --of /mnt/data2/sarah/aDNA/Bger/results/genome_delta --prefix bger_all --t 20 > /mnt/data2/sarah/aDNA/Bger/results/genome_delta/genomedelta_bger_all.log 2>&1 &

#with the original GD from riccardos folder (can only be accessed with his user) and with the main-sarah.sh script to exclude scaffolds with no coverage
nohup bash /home/riccardo/programs/GenomeDelta/linux/main-sarah.sh --fq /mnt/data2/sarah/aDNA/Bger/processed/genome_delta/Bger_combined_all_reads.fastq.gz --fa /mnt/data2/sarah/aDNA/Bger/raw/ref_genome/GCA_000762945.2_Bger_2.0_genomic.fna --of /mnt/data2/sarah/aDNA/Bger/results/genome_delta/genome_delta --prefix bger_all --t 20 > /mnt/data2/sarah/aDNA/Bger/results/genome_delta/genomedelta_bger_all.log 2>&1 &

#when mapping is already done
 nohup bash /home/riccardo/programs/GenomeDelta/linux/main-sarah.sh --bam /mnt/data2/sarah/aDNA/Bger/results/genome_delta/bger_all.sorted.bam --fa /mnt/data2/sarah/aDNA/Bger/raw/ref_genome/GCA_000762945.2_Bger_2.0_genomic.fna --of /mnt/data2/sarah/aDNA/Bger/results/genome_delta/genome_delta --prefix bger_all --t 20 > /mnt/data2/sarah/aDNA/Bger/results/genome_delta/genomedelta_bger_all_bam.log 2>&1 &

 # current main-sarah.sh bam-to-fasta.sh has some stuff outcommented!
 # for running it again from the beginning, remove the #

 # ONLY RUN GENOMEDELTA IN THE CONDA ENVIRONMET (conda activate Genomedelta)
 # (the newst/working version of the softwares were only tested there)