library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)
library(yaml) # Load the yaml library

process_and_plot_before_after <- function(analysis_files, output_folder, species_names, comparison_name) {
  before_after_data <- list()
  
  for (i in 1:length(analysis_files)) {
    filepath <- analysis_files[i]
    if (file.exists(filepath)) {
      df <- read.table(filepath, sep ="\t", header = TRUE)
      df$species_id <- names(species_names)[i] #get the species ID
      df$species <- species_names[[i]]  # Get species long name from the provided list
      before_after_data[[df$species_id[1]]] <- df # use species id to store
    } else {
      warning(paste("File not found:", filepath))
    }
  }
  
  df_before_after <- bind_rows(before_after_data)

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

root_folder <- args[1]
config_file <- args[2] #  argument for the config file
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

# Iterate through the comparisons in the config file.
for (comparison_name in names(config$compare_species)) {
  comparison_data <- config$compare_species[[comparison_name]]
  
  # Construct full paths to analysis files and extract species names and long names.
  analysis_files <- sapply(names(comparison_data), function(species_id) {
    species_folder <- config$species[[species_id]]$folder_name
    file.path(root_folder, species_folder, "results", "qualitycontrol", paste0(species_id,"_reads_processing_result.tsv"))
  })

  species_names <- sapply(names(comparison_data), function(species_id) {
    config$species[[species_id]]$name
  })
  names(species_names) <- names(comparison_data)
  
  # Check if analysis_files is empty
  if (length(analysis_files) == 0) {
    warning(paste("No analysis files found for comparison:", comparison_name))
    next # Skip to the next comparison
  }

    # Information about the species analyzed to console
  cat("Species analyzed for comparison:", comparison_name, "\n")
  cat("Species IDs:", names(species_names), "\n")
  cat("Species long names:", species_names, "\n")
  cat("Analysis files:", analysis_files, "\n")

  process_and_plot_before_after(analysis_files, output_folder, species_names, comparison_name)
}

