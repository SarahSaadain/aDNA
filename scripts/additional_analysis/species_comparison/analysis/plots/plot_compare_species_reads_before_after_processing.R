library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)
library(yaml) # Load the yaml library

process_and_plot_before_after <- function(analysis_files, output_folder, species_names, comparison_name) {
  list_of_analysis_dataframes <- list()
  
  for (i in 1:length(analysis_files)) {
    filepath <- analysis_files[i]

    print(paste("Processing file:", filepath))

    if (file.exists(filepath)) {
      df <- read.table(
        filepath,
        sep = "\t",
        header = TRUE,
        colClasses = c(individual = "character", protocol = "character")
      )
      df$species_id <- names(species_names)[i] #get the species ID
      df$species <- species_names[[i]]  # Get species long name from the provided list
      list_of_analysis_dataframes[[df$species_id[1]]] <- df # use species id to store
    } else {
      stop(paste("File not found:", filepath))
    }
  }
  
  df_before_after <- bind_rows(list_of_analysis_dataframes)

  #check if the species column exists
  if (!("species" %in% colnames(df_before_after))){
    stop("Error: 'species' column not found in the dataframes.  Check the input files.")
  }

  # Create a factor for the 'species' column, defining the order of the levels.
  if (!is.null(species_names)) {
    desired_order = unname(species_names) # use the long names for ordering
    df_before_after$species <- factor(df_before_after$species, levels = desired_order)
  }
  
  df_species <- df_before_after %>%
    group_by(species) %>%
    summarise(raw_count_absolute = sum(raw_count),
              adapter_removed_count_absolute = sum(adapter_removed_count),
              duplicates_removed_count_absolute = sum(duplicates_removed_count),
              .groups = "drop")
  
  df_long_species <- df_species %>%
    pivot_longer(
      cols = c(raw_count_absolute,
               adapter_removed_count_absolute,
               duplicates_removed_count_absolute),
      names_to = "read_type", values_to = "count"
    )
  
  df_long_species <- df_long_species %>%
    mutate(
      read_type = factor(
        read_type, levels = c("raw_count_absolute",
                              "adapter_removed_count_absolute",
                              "duplicates_removed_count_absolute")))

  # Create a factor for the 'species' column, defining the order of the levels.
  if (!is.null(species_names)) {
    desired_order = unname(species_names) # use the long names for ordering
    df_long_species$species <- factor(df_long_species$species, levels = desired_order)
  }                            
  
  plot_before_after <- ggplot(df_long_species, aes(x = species, y = count, fill = read_type)) +
    geom_bar(stat = "identity", position = position_dodge(preserve = "single")) +
    scale_fill_manual(
      values = c("raw_count_absolute" = "darkblue",
                 "adapter_removed_count_absolute" = "#007FFF",
                 "duplicates_removed_count_absolute" = "#00FFEF"),
      labels = c("raw_reads",
                 "reads_after_adapterremoval",
                 "reads_after_duplicationremoval")
    ) +
    scale_y_continuous(labels = scales::comma) +
    labs(x = "Species", y = "Read Count", fill = "Read Type", title = "Read count raw vs after processing") +
    theme_bw() +
    theme(axis.text.x = element_text(size = 18, angle = 45, vjust = 1, hjust = 1),
          legend.text = element_text(size = 18),
          axis.text.y = element_text(size = 18),
          axis.title.x = element_text(size = 20, face = "bold"),
          axis.title.y = element_text(size = 20, face = "bold"),
          plot.title = element_text(size = 24, face = "bold", hjust = 0.5),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black"))
  
  ggsave(file.path(output_folder, paste0("plot_before_after_", paste(comparison_name, collapse = "_"), ".png")), plot_before_after, width = 12, height = 8, dpi = 300)
}



# Command line argument handling
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <output_folder> <config_file> <root_folder>")
}

adna_project_folder_path <- args[1]
adna_config_file <- args[2] #  argument for the config file
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

# Loop over each species comparison defined in the config file.
# Each comparison involves a group of species to be analyzed together.
for (comparison_name in names(config$compare_species)) {
  
  # Get the list of species for the current comparison.
  comparison_data <- config$compare_species[[comparison_name]]
  
  # For each species in this comparison, construct the full path to its processing result file.
  analysis_files <- sapply(names(comparison_data), function(species_id) {
    
    # Get the folder name where the species' data is stored (defined in config).
    species_folder <- config$species[[species_id]]$folder_name
    
    # Build the full path to the reads processing result TSV file.
    # Format: root_folder/species_folder/results/qualitycontrol/processed_reads/{species_id}_reads_processing_result.tsv
    file.path(
      adna_project_folder_path,
      species_folder,
      "results",
      "qualitycontrol",
      "processed_reads",
      paste0(species_id, "_reads_processing_result.tsv")
    )
  })

  # Get the full (long) names of the species from the config file
  # to use for plots, labels, or printed output.
  species_names <- sapply(names(comparison_data), function(species_id) {
    config$species[[species_id]]$name
  })

  # Name each entry in the species_names vector with its corresponding species ID.
  # This preserves the relationship between species_id and readable name.
  names(species_names) <- names(comparison_data)
  
  # If no analysis files were found for this comparison (e.g., misconfiguration),
  # print a warning and skip to the next comparison in the loop.
  if (length(analysis_files) == 0) {
    warning(paste("No analysis files found for comparison:", comparison_name))
    next
  }

  # Print summary information to the console for transparency/debugging.
  cat("Species analyzed for comparison:", comparison_name, "\n")
  cat("Species IDs:", names(species_names), "\n")
  cat("Species long names:", species_names, "\n")
  cat("Analysis files:", analysis_files, "\n")

  # Call a custom function to process the TSV files and generate a "before/after" plot.
  # This function is assumed to handle file reading, data processing, and visualization.
  process_and_plot_before_after(
    analysis_files,   # Vector of file paths for this comparison
    output_folder_path_for_plots,    # Destination folder for saving the plot
    species_names,    # Named vector of species long names
    comparison_name   # Name of the current comparison, for labeling
  )

  print(paste("Before/after plot saved for comparison:", comparison_name))
}


