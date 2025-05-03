library(dplyr)
library(ggplot2)
library(scales)
library(stringr)
library(yaml) # Load the yaml library

process_and_plot_depth_breadth <- function(analysis_files, output_folder, species_names, comparison_name) {
  depth_breadth_data <- list()
  
  for (i in 1:length(analysis_files)) {
    filepath <- analysis_files[i]
    if (file.exists(filepath)) {
      df <- read.table(filepath, header = TRUE)
      df$species_id <- names(species_names)[i] #get the species ID
      df$species <- species_names[[i]]  # Get species long name from the provided list
      depth_breadth_data[[df$species_id[1]]] <- df # use species id to store
    } else {
      warning(paste("File not found:", filepath))
    }
  }
  
  all_data <- bind_rows(depth_breadth_data)
  
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
    ref_genome_name <- tools::file_path_sans_ext(basename(comparison_data[[species_name]]$reference_genome))
    file.path(root_folder, species_folder, "results", ref_genome_name, "coverage_depth_breadth", paste0(species_id, "_combined_coverage_analysis.csv"))
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
  cat("Reference genomes:", sapply(names(comparison_data), function(species_id) {
    comparison_data[[species_id]]$reference_genome
  }), "\n")
  
  process_and_plot_depth_breadth(analysis_files, output_folder, species_names, comparison_name)
}
