##aDNA sequence length distribution plot##

#load libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)  # for number formatting


plot_sequence_length_distribution <- function(species, source_file, target_folder) {
  
  print("Executing plot_sequence_length_distribution")
  
  # Read the source file
  file <- read.table(source_file, header = TRUE)

  # Collapse 1 and 2
  file <- file %>%
    mutate(protocol_collapsed = gsub("[12]$", "", protocol))

  # Summarize read counts for each length and sample
  df_protocol <- file %>%
    group_by(protocol_collapsed) %>%
    summarise(raw_count_absolute = sum(raw_count),
              adapter_removed_count_absolute = sum(adapter_removed_count),
              duplicates_removed_count_absolute = sum(duplicates_removed_count),
              .groups = "drop")  # Count the number of reads for each length

  df_long <- df_protocol %>%
    pivot_longer(
      cols = c(raw_count_absolute, 
                adapter_removed_count_absolute,
                duplicates_removed_count_absolute),
      names_to = "read_type", values_to = "count"
    )

  df_long <- df_long %>%
    mutate(
      read_type = factor(
        read_type, levels = c("raw_count_absolute", 
                                "adapter_removed_count_absolute",
                                "duplicates_removed_count_absolute")))

  # Create the plot
  # Create the plot
  p <- ggplot(df_long, aes(x = protocol_collapsed, y = count, fill = read_type)) +
    geom_bar(stat = "identity", position = position_dodge(preserve = "single")) +  # Ensures consistent grouping order
    scale_fill_manual(values = c("raw_count_absolute" = "#1f77b4",    # Blue
                                 "adapter_removed_count_absolute" = "#ff7f0e",  # Orange
                                 "duplicates_removed_count_absolute" = "#2ca02c")) +  # Green
    scale_y_continuous(labels = scales::comma) +  # Format y-axis labels with commas
    labs(x = "Protocol", y = "Read Count", fill = "Read Type") +
    theme_bw() +  # Use a white background
    theme(panel.grid.major = element_line(color = "grey90"),  # Light grid lines
          panel.grid.minor = element_blank())
  
    file_name <- paste(species, "_sequence_length_distribution.png")
    file_path <- file.path(target_folder, file_name)
    
    # Save the plot
    ggsave(file_path, plot = p, width = 8, height = 5, dpi = 300)
}

# FOR TESTING
# plot_sequence_length_distribution(
#   "Bger",
#   "/Users/ssaadain/Documents/aDNA/Bger/results/processed_reads/Bger_reads_processing_result.tsv",
#   "/Users/ssaadain/Documents/aDNA/Bger/results/plots/processed_reads"
# )


# Ensure you capture command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the correct number of arguments are passed
if (length(args) < 3) {
  stop("Not enough arguments. Required: species, depth_file, target_folder.")
}

# Assign the arguments to variables
species <- args[1]
reads_analysis_file <- args[2]
target_folder <- args[3]

plot_sequence_length_distribution(
  species,
  reads_analysis_file,
  target_folder
)


