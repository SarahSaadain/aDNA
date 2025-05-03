#!/usr/bin/env Rscript

library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(stringr)
library(scales)
library(yaml) # Load the yaml library

process_and_plot_endogenous_reads <- function(analysis_files, output_folder, species_names, comparison_name) {
  # Initialize an empty list to store data frames
  endogenous_data <- list()
  
  # Iterate over each analysis file
  for (i in 1:length(analysis_files)) {
    file_path <- analysis_files[i]
    
    # Check if the file exists
    if (file.exists(file_path)) {
      # Read the CSV file
      df <- read.csv(file_path, header = FALSE)
      
      # Assign column names
      col_names <- c("sample", "endogenous", "total", "percent_endogenous")
      colnames(df) <- col_names
      
      df$species_id <- names(species_names)[i]  # Get species ID
      df$species <- species_names[[i]] #get species long name
      
      endogenous_data[[df$species_id[1]]] <- df
      
    } else {
      # Print a warning if the file does not exist
      warning(paste("File not found:", file_path))
    }
  }
  
  # Combine all data frames into one data frame
  df_combined <- bind_rows(endogenous_data)
  
  # Create a new column combining species and sample name for x-axis labels.  Use species long name.
  df_combined$label <- paste(df_combined$species, df_combined$sample, sep = "_")
  
  # Convert percent_endogenous to percentage
  df_combined$percent_endogenous <- df_combined$percent_endogenous * 100
  
  # Create a factor for the 'species' column, defining the order of the levels.
  if (!is.null(species_names)) {
    desired_order = unname(species_names)  # Use long names for ordering
    df_combined$species <- factor(df_combined$species, levels = desired_order)
  }
  
  # Define a color palette for species.  Make it dynamic.
  num_species <- length(unique(df_combined$species))
  if (num_species <= 8) {
    species_colors <- c("salmon", "orange", "chartreuse3", "darkgreen", "darkblue", "grey", "darkorchid", "cyan")[1:num_species]
  } else {
    species_colors <- colorRampPalette(c("salmon", "orange", "chartreuse3", "darkgreen", "darkblue", "grey", "darkorchid", "cyan"))(num_species)
  }
  names(species_colors) <- levels(df_combined$species)
  
  # Reorder labels based on desired species order
  df_combined$label <- factor(df_combined$label, levels = df_combined$label[order(match(df_combined$species, desired_order))])
  
  # Create the plot
  endogenous_plot <- ggplot(df_combined, aes(x = species, y = percent_endogenous, fill = species)) +
    geom_bar(stat = "identity", position = "dodge") +
    theme_classic(base_size = 16) +
    labs(x = "Species", y = "Percentage of Endogenous Reads", title = paste("Endogenous Reads Across Species - ", comparison_name)) +
    theme(axis.text.x = element_text(size = 14, angle = 45, vjust = 1, hjust = 1),
          axis.text.y = element_text(size = 16),
          axis.title.x = element_text(size = 18, face = "bold"),
          axis.title.y = element_text(size = 18, face = "bold"),
          plot.title = element_text(size = 22, face = "bold", hjust = 0.5),
          legend.position = "none",
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black")) +
    scale_fill_manual(values = species_colors)
  
  # Print the plot
  #print(endogenous_plot)
  
  # Save the plot to the specified output folder
  ggsave(file.path(output_folder, paste0("plot_endogenous_reads_", comparison_name, ".png")), endogenous_plot, width = 12, height = 8, dpi = 300)
}

# Command line argument handling
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <root_folder> <config_file> <output_folder>")
}

root_folder <- args[1]
config_file <- args[2]
output_folder <- args[3]

# Create the output directory if it doesn't exist
if (!dir.exists(output_folder)) {
  dir.create(output_folder, recursive = TRUE)
}

# Check if the root folder exists
if (!dir.exists(root_folder)) {
  stop(paste("Root folder does not exist:", root_folder))
}

# Check if the config file exists
if (!file.exists(config_file)) {
  stop(paste("Config file does not exist:", config_file))
}

# Read the config file
config <- yaml.load_file(config_file) # Load the config file

# Check if any relevant configuration is present
if (is.null(config$compare_species) || length(config$compare_species) == 0) {
  stop("No comparisons found in the config file.")
}

# Iterate through the comparisons
for (comparison_name in names(config$compare_species)) {
  comparison_data <- config$compare_species[[comparison_name]]
  
  # Construct full paths to analysis files and extract species names.
  analysis_files <- sapply(names(comparison_data), function(species_name) {
    species_folder <- config$species[[species_name]]$folder_name
    ref_genome_name <- str_replace(basename(comparison_data[[species_name]]$reference_genome), "\\..*$", "")
    file.path(root_folder, species_folder, "results", ref_genome_name, "endogenous_reads", paste0(species_name, "_combined_endogenous_reads.csv"))
  })
  
  # Extract species names
  species_names <- sapply(names(comparison_data), function(species_id) {
    config$species[[species_id]]$name
  })
  names(species_names) <- names(comparison_data)
  
  # Check if analysis_files is empty
  if (length(analysis_files) == 0) {
    warning(paste("No analysis files found for comparison:", comparison_name))
    next
  }
  
  # Call the function
  process_and_plot_endogenous_reads(analysis_files, output_folder, species_names, comparison_name)
}
