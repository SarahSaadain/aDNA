import common.config_manager as config_manager  # Assuming config_manager.py is in the same directory

# Load the configuration file (only once)
try:
    config = config_manager.load_config('config.yaml')  # Or however you specify the path
    print("Config loaded successfully.")
    #print("Loaded Configuration:")
    #print(config)

    print("Project path: ", config['path_adna_project'])
    print("Species: ", list(config['species'].keys()))

except FileNotFoundError:
    print("Config file not found.  Exiting.")
    exit(1) #Or handle more gracefully

#####################
# Constants
#####################

PATH_ADNA_PROJECT = config['path_adna_project']
#PATH_ADNA_PROJECT = "/mnt/data2/sarah/aDNA"
#PATH_ADNA_PROJECT = "/Users/ssaadain/Documents/aDNA"

# config
THREADS_DEFAULT = config['threads_default']

# species folders
#FOLDER_BGER = "Bger" # just the species names, could be in /raw or in /processed
#FOLDER_DSIM = "Dsim"
#FOLDER_PHORTICA = "Phortica"
#FOLDER_SEPSIS = "Sepsis"
#FOLDER_MMUS = "Mmus"
#FOLDER_DMEL = "Dmel"
#FOLDER_TRIAL_BGER = "trial_Bger"
#FOLDER_TRIAL_DSIM = "trial_Dsim"
#FOLDER_TRIAL_PHORTICA = "trial_Phortica"
#FOLDER_TRIAL_SEPSIS = "trial_Sepsis"
#FOLDER_TRIAL_MMUS = "trial_Mmus"
#FOLDER_TRIAL_DMEL = "trial_Dmel"

FOLDER_SPECIES = list(config['species'].keys())
#FOLDER_SPECIES = [FOLDER_BGER, FOLDER_DSIM, FOLDER_PHORTICA, FOLDER_SEPSIS, FOLDER_MMUS, FOLDER_DMEL, FOLDER_TRIAL_BGER, FOLDER_TRIAL_DSIM, FOLDER_TRIAL_PHORTICA, FOLDER_TRIAL_SEPSIS, FOLDER_TRIAL_MMUS, FOLDER_TRIAL_DMEL]

PROGRAM_PATH_CUTADAPT = config['tools']['cutadapt']
PROGRAM_PATH_FASTP = config['tools']['fastp']
PROGRAM_PATH_SGA = config['tools']['sga']
PROGRAM_PATH_MULTIQC = config['tools']['multiqc']
PROGRAM_PATH_FASTQC = config['tools']['fastqc']
PROGRAM_PATH_BWA = config['tools']['bwa']
PROGRAM_PATH_BEDTOOLS = config['tools']['bedtools']
PROGRAM_PATH_BWA_MEM = "mem"
PROGRAM_PATH_SAMTOOLS = config['tools']['samtools']
PROGRAM_PATH_SAMTOOLS_FAIDX =  "faidx"
PROGRAM_PATH_SAMTOOLS_VIEW =  "view"
PROGRAM_PATH_SAMTOOLS_SORT = "sort"
PROGRAM_PATH_SAMTOOLS_INDEX = "index"
PROGRAM_PATH_ANGSD = config['tools']['angsd']
PROGRAM_PATH_SEQKIT = config['tools']['seqkit']
PROGRAM_PATH_SEQKIT_STATS = "stats"
