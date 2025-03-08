# Load required libraries
library(ggplot2)
library(tidyr)
library(readr)
library(tools)  # For file path manipulation
library(dplyr)  # For data manipulation

# Function to generate and save plots
plot_read_length_distribution <- function(source_file, output_folder) {
  # Read the TSV data
  df <- read_tsv(source_file, col_types = cols(), show_col_types = FALSE)  # Suppress messages
  
  # Check if required columns exist
  required_cols <- c("file", "length", "adapter_removed", "quality_check", "duplicates_removed")
  if (!all(required_cols %in% colnames(df))) {
    stop("Error: The input file must contain the columns: file, length, adapter_removed, quality_check, duplicates_removed")
  }
  
  # Ensure the output folder exists
  if (!dir.exists(output_folder)) {
    dir.create(output_folder, recursive = TRUE)
  }
  
  # Reshape data from wide to long format
  df_long <- pivot_longer(df, cols = c("adapter_removed", "quality_check", "duplicates_removed"),
                          names_to = "Processing_Step", values_to = "Count")

  # Generate a plot for each unique file
  unique_files <- unique(df$file)
  for (file_name in unique_files) {
    df_subset <- df_long %>% filter(file == file_name)  # Filter data for this file
    
    p <- ggplot(df_subset, aes(x = length, y = Count, color = Processing_Step, group = Processing_Step)) +
      geom_line() +
      geom_point() +
      theme_minimal() +
      labs(title = paste("Read Length Distribution:", file_name),
           x = "Read Length",
           y = "Count",
           color = "Processing Step") +
      scale_x_continuous(breaks = seq(min(df_subset$length, na.rm = TRUE), max(df_subset$length, na.rm = TRUE), by = 5))
    
    # Generate output filename
    output_file <- file.path(output_folder, paste0(file_name, ".png"))
    
    # Save the plot
    ggsave(output_file, plot = p, width = 8, height = 6, dpi = 300)
    
    # Print message
    message("Plot saved to: ", output_file)
  }

  # Aggregate (sum up) counts for the combined plot across all files
  df_combined <- df_long %>%
    group_by(length, Processing_Step) %>%
    summarise(Count = sum(Count, na.rm = TRUE), .groups = "drop")

  # Create a combined plot
  p_combined <- ggplot(df_combined, aes(x = length, y = Count, color = Processing_Step, group = Processing_Step)) +
    geom_line(alpha = 0.7) +
    geom_point(alpha = 0.7) +
    theme_minimal() +
    labs(title = "Combined Read Length Distribution Across All Files",
         x = "Read Length",
         y = "Total Count",
         color = "Processing Step") +
    scale_x_continuous(breaks = seq(min(df_combined$length, na.rm = TRUE), max(df_combined$length, na.rm = TRUE), by = 5))

  # Generate output filename for the combined plot (same as input file, replacing .tsv with .png)
  combined_output_file <- file.path(output_folder, paste0(file_path_sans_ext(basename(source_file)), ".png"))

  # Save the combined plot
  ggsave(combined_output_file, plot = p_combined, width = 10, height = 8, dpi = 300)

  # Print message
  message("Combined plot saved to: ", combined_output_file)
}

# Get command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if two arguments are provided
if (length(args) != 2) {
  stop("Usage: Rscript plot_reads.R <source_file.tsv> <output_folder>")
}

# Assign arguments
source_file <- args[1]
output_folder <- args[2]

# Run the function
plot_read_length_distribution(source_file, output_folder)
