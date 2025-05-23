library(dplyr)
library(ggplot2)
library(scales)
library(stringr)
library(yaml) # Load the yaml library

process_and_plot_depth_breadth <- function(analysis_files, output_folder, species_names, comparison_name) {
  list_of_analysis_dataframes <- list()
  
  for (i in 1:length(analysis_files)) {
    filepath <- analysis_files[i]

    print(paste("Processing file:", filepath))

    if (file.exists(filepath)) {
      df <- read.table(filepath, sep =",", header = TRUE)
      df$species_id <- names(species_names)[i] #get the species ID
      df$species <- species_names[[i]]  # Get species long name from the provided list
      list_of_analysis_dataframes[[df$species_id[1]]] <- df # use species id to store
    } else {
      stop(paste("File not found:", filepath))
    }
  }
  
  all_data <- bind_rows(list_of_analysis_dataframes)
  
  #check if the species column exists
  if (!("species" %in% colnames(all_data))){
    stop("Error: 'species' column not found in the dataframes.  Check the input files.")
  }
  
  # Create a factor for the 'species' column, defining the order of the levels.
  if (!is.null(species_names)) {
    desired_order = unname(species_names) # use the long names for ordering
    all_data$species <- factor(all_data$species, levels = desired_order)
  }
  
  # Generate a color scale with a maximum of 8 distinct colors
  num_species <- length(unique(all_data$species))
  if (num_species <= 8) {
    species_colors <- c("salmon", "orange", "chartreuse3", "darkgreen", "darkblue", "grey", "darkorchid", "cyan")[1:num_species]
  } else {
    # If there are more than 8 species, generate a palette of distinct colors
    species_colors <- colorRampPalette(c("salmon", "orange", "chartreuse3", "darkgreen", "darkblue", "grey", "darkorchid", "cyan"))(num_species)
  }
  names(species_colors) <- levels(all_data$species) # Ensure names match factor levels
  
  # Plot breadth
  plot_breadth <- ggplot(all_data, aes(x = factor(species), y = percent_covered, fill = species)) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Percent Covered") +
    xlab("Species") +
    ggtitle(paste("Distribution of Percent Covered - ", comparison_name)) +
    theme(axis.text.x = element_text(size = 18, angle = 45, vjust = 1, hjust = 1),
          legend.text = element_text(size = 18),
          axis.text.y = element_text(size = 18),
          axis.title.x = element_text(size = 20, face = "bold"),
          axis.title.y = element_text(size = 20, face = "bold"),
          plot.title = element_text(size = 24, face = "bold", hjust = 0.5),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black"),
          legend.position = "none") +
    scale_fill_manual(values = species_colors)
  
  #print(plot_breadth)
  ggsave(file.path(output_folder, paste0("plot_breadth_", comparison_name, ".png")), plot_breadth, width = 12, height = 8, dpi = 300)
  
  # Plot depth
  plot_depth <- ggplot(all_data, aes(x = factor(species), y = avg_depth, fill = species)) +
    scale_y_continuous(
      trans = "log10",
      breaks = scales::trans_breaks("log10", function(x) 10^x),
      labels = scales::comma
    ) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Avg. Depth") +
    xlab("Species") +
    ggtitle(paste("Distribution of Average Depth - ", comparison_name)) +
    theme(axis.text.x = element_text(size = 18, angle = 45, vjust = 1, hjust = 1),
          legend.text = element_text(size = 18),
          axis.text.y = element_text(size = 18),
          axis.title.x = element_text(size = 20, face = "bold"),
          axis.title.y = element_text(size = 20, face = "bold"),
          plot.title = element_text(size = 24, face = "bold", hjust = 0.5),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black"),
          legend.position = "none") +
    scale_fill_manual(values = species_colors)
  
  ggsave(file.path(output_folder, paste0("plot_depth_", comparison_name, ".png")), plot_depth, width = 12, height = 8, dpi = 300)
}

# Command line argument handling
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <output_folder> <config_file> <root_folder>")
}

adna_project_folder_path <- args[1]
adna_project_config_file <- args[2] #  argument for the config file
output_folder_path_for_plots <- args[3]

# Create the output directory if it doesn't exist
if (!dir.exists(output_folder_path_for_plots)) {
  dir.create(output_folder_path_for_plots, recursive = TRUE)
}

# Check if the aDNA project folder exists
if (!dir.exists(adna_project_folder_path)) {
  stop(paste("aDNA project folder does not exist:", adna_project_folder_path))
}

# Check if the aDNA project config file exists
if (!file.exists(adna_project_config_file)) {
  stop(paste("aDNA project config file does not exist:", adna_project_config_file))
}

# Read the config file
config <- yaml.load_file(adna_project_config_file) # Load the config file

# Check if any relevant configuration is present
if (is.null(config$compare_species) || length(config$compare_species) == 0) {
  stop("No comparisons found in the config file.")
}

# Iterate through each comparison defined in the config file's 'compare_species' section.
# Each comparison represents a set of species to be analyzed together.
for (comparison_name in names(config$compare_species)) {
  
  # Retrieve the list of entries involved in this specific comparison.
  comparison_data <- config$compare_species[[comparison_name]]
  
  # Initialize empty lists to store the file paths and species names.
  # Using lists first allows for flexible construction before converting to named vectors.
  analysis_files_list <- list()
  species_names_list <- list()
  
  # Iterate through each entry within the current comparison.
  for (comparison_entry_key in names(comparison_data)) {
    current_entry_details <- comparison_data[[comparison_entry_key]]
    
    # Determine the actual species_id to be used for looking up details in config$species.
    # It first checks if 'species_id' is explicitly provided within the current entry's details.
    # If not, it defaults to using the 'comparison_entry_key' itself as the species_id.
    actual_species_id <- if (!is.null(current_entry_details$species_id) && current_entry_details$species_id != "") {
      current_entry_details$species_id
    } else {
      comparison_entry_key
    }
    
    # Get the folder name for the determined 'actual_species_id' from the main config$species section.
    species_folder <- config$species[[actual_species_id]]$folder_name
    
    # Extract the base name (filename without extension) of the reference genome file
    # specified for the current comparison entry.
    ref_genome_name <- tools::file_path_sans_ext(basename(current_entry_details$reference_genome))
    
    # Construct the full file path to the extended coverage analysis file for this entry.
    # The 'species_id' used in the filename part of the path is the 'actual_species_id'.
    file_path <- file.path(
      adna_project_folder_path,
      species_folder,
      "results",
      ref_genome_name,
      "coverage_depth_breadth",
      paste0(
        actual_species_id, "_combined.fastq_", ref_genome_name, "_extended_coverage_analysis.csv"
      )
    )
    # Store the constructed file path in the list, using the original 'comparison_entry_key'
    # as the name. This key is what defines the relationship within the comparison.
    analysis_files_list[[comparison_entry_key]] <- file_path
    
    # Get the user-friendly species name from the main config$species section.
    # This name will be used as a base for generating a unique plot label.
    display_name_from_config <- config$species[[actual_species_id]]$name
    if (is.null(display_name_from_config) || display_name_from_config == "") {
      display_name_from_config <- actual_species_id # Fallback if no display name is found
    }
    
    # Determine the label for plotting (value in species_names_list).
    # This logic aims to create a unique and informative label to prevent "duplicated factor level" errors.
    if (!is.null(current_entry_details$species_id) && current_entry_details$species_id != "") {
        # If species_id was explicitly given, concatenate comparison_entry_key with the display name.
        # This makes the label unique if multiple entries refer to the same actual_species_id.
        species_names_list[[comparison_entry_key]] <- paste0(comparison_entry_key, " ", display_name_from_config)
    } else {
        # If species_id was NOT explicitly given, use the display_name_from_config directly.
        species_names_list[[comparison_entry_key]] <- display_name_from_config
    }
  }
  
  # Convert the lists of file paths and species names into named vectors.
  # This makes them suitable for functions that expect named vectors (e.g., for plotting).
  analysis_files <- unlist(analysis_files_list)
  species_names <- unlist(species_names_list)
  
  # Check if the list of analysis files is empty after processing all entries.
  # If so, issue a warning and skip to the next comparison.
  if (length(analysis_files) == 0) {
    warning(paste("No analysis files found for comparison:", comparison_name))
    next  # Continue to the next comparison in the loop
  }

  # Log information about the species analyzed to the console for debugging/monitoring.
  cat("Species analyzed for comparison:", comparison_name, "\n")
  # Note: names(species_names) will correspond to the 'comparison_entry_key'
  cat("Comparison Entry Keys:", names(species_names), "\n")
  cat("Species Display Names:", species_names, "\n")
  cat("Analysis files:", analysis_files, "\n")
  
  # Log the reference genomes used for each entry in the comparison.
  # This uses the original 'comparison_entry_key' to access the 'reference_genome' from 'comparison_data'.
  cat("Reference genomes:", sapply(names(comparison_data), function(comparison_entry_key) {
    comparison_data[[comparison_entry_key]]$reference_genome
  }), "\n")
  
  # Call the plotting function with the collected data.
  process_and_plot_depth_breadth(
    analysis_files,           # Vector of file paths for this comparison
    output_folder_path_for_plots,    # Destination folder for saving the plot
    species_names,            # Named vector of user-friendly species names
    comparison_name           # Name of the current comparison, for labeling
  )

  print(paste("Depth and breadth plot saved for comparison:", comparison_name))
}
