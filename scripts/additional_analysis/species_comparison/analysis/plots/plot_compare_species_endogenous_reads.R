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
  list_of_analysis_dataframes <- list()
  
  # Iterate over each analysis file
  for (i in 1:length(analysis_files)) {
    file_path <- analysis_files[i]

    print(paste("Processing file:", file_path))
    
    # Check if the file exists
    if (file.exists(file_path)) {
      # Read the CSV file, now with header=TRUE
      df <- read.csv(file_path, header = TRUE)
      
      # Assign column names to the expected names
      col_names <- c("sample", "endogenous", "total", "percent_endogenous")

      # Check if the file contains the expected columns.  If not, error.
      if (!all(c("Filename", "MappedReads", "TotalReads", "Proportion") %in% colnames(df))){
        stop(paste("File", file_path, "does not contain the expected columns: Filename, MappedReads, TotalReads, Proportion. Please check the input data."))
      }
      
      # Rename the columns to standard names
      df <- df %>%
        rename(
          sample = Filename,
          endogenous = MappedReads,
          total = TotalReads,
          percent_endogenous = Proportion
        )
      
      df$species_id <- names(species_names)[i]  # Get species ID
      df$species <- species_names[[i]] #get species long name
      
      list_of_analysis_dataframes[[df$species_id[1]]] <- df
      
    } else {
      # Print a warning if the file does not exist
      stop(paste("File not found:", file_path))
    }
  }
  
  # Combine all data frames into one data frame
  df_combined <- bind_rows(list_of_analysis_dataframes)
  
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

adna_project_folder_path <- args[1]
adna_config_file <- args[2]
output_folder_path_for_plots <- args[3]

# Create the output directory if it doesn't exist
if (!dir.exists(output_folder_path_for_plots)) {
  dir.create(output_folder_path_for_plots, recursive = TRUE)
}

# Check if the root folder exists
if (!dir.exists(adna_project_folder_path)) {
  stop(paste("Root folder does not exist:", adna_project_folder_path))
}

# Check if the config file exists
if (!file.exists(adna_config_file)) {
  stop(paste("Config file does not exist:", adna_config_file))
}

# Read the config file
config <- yaml.load_file(adna_config_file) # Load the config file

# Check if any relevant configuration is present
if (is.null(config$compare_species) || length(config$compare_species) == 0) {
  stop("No comparisons found in the config file.")
}

# Loop over each species comparison defined in the config's 'compare_species' section.
# Each entry defines a group of species to compare for endogenous reads.
for (comparison_name in names(config$compare_species)) {
  
  # Retrieve the species data for this comparison.
  # Each item includes the species ID and its associated reference genome.
  comparison_data <- config$compare_species[[comparison_name]]
  
  # For each species in the comparison, construct the path to its endogenous reads file.
  analysis_files <- sapply(names(comparison_data), function(species_name) {
    
    # Get the name of the folder corresponding to the current species.
    species_folder <- config$species[[species_name]]$folder_name
    
    # Get the reference genome file name (without its extension).
    # This is used to help construct the file path.
    ref_genome_name <- tools::file_path_sans_ext(basename(comparison_data[[species_name]]$reference_genome))
    
    # Build the full file path to the endogenous reads CSV file for this species.
    # Format: root_folder/species_folder/results/ref_genome_name/endogenous_reads/{species_name}_combined_endogenous_reads.csv
    file.path(
      adna_project_folder_path,
      species_folder,
      "results",
      ref_genome_name,
      "endogenous_reads",
      paste0(species_name, "_endogenous_reads.csv")
    )
  })

  # Get the readable (long) names of each species involved in the comparison,
  # for display in plots, legends, or reports.
  species_names <- sapply(names(comparison_data), function(species_id) {
    config$species[[species_id]]$name
  })

  # Assign species IDs as names of the species_names vector,
  # maintaining a mapping between IDs and readable names.
  names(species_names) <- names(comparison_data)
  
  # If no analysis files were generated (empty list), issue a warning and skip this comparison.
  if (length(analysis_files) == 0) {
    warning(paste("No analysis files found for comparison:", comparison_name))
    next  # Proceed to the next comparison
  }

  # Information about the species analyzed to console
  cat("Species analyzed for comparison:", comparison_name, "\n")
  cat("Species IDs:", names(species_names), "\n")
  cat("Species long names:", species_names, "\n")
  cat("Analysis files:", analysis_files, "\n")
  cat("Reference genomes:", sapply(names(comparison_data), function(species_id) {
    comparison_data[[species_id]]$reference_genome
  }), "\n")
  
  # Call the function
  process_and_plot_endogenous_reads(
    analysis_files,   # Vector of file paths for this comparison
    output_folder_path_for_plots,    # Destination folder for saving the plot
    species_names,    # Named vector of species long names
    comparison_name   # Name of the current comparison, for labeling
  )

  print(paste("Endogenous reads plot saved for comparison:", comparison_name))
}
