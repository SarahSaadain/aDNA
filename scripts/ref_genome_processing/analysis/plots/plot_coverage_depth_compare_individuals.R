library(tidyverse)
library(ggplot2)
library(tools)

# Violin plot function
plot_depth_coverage_violon <- function(df_depth_combined) {
  ggplot(df_depth_combined, aes(x = factor(individual), y = avg_depth)) +
    scale_y_continuous(
      trans = "log10",
      breaks = scales::trans_breaks("log10", function(x) 10^x),
      labels = scales::comma
    ) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Avg. Depth") +
    xlab("Individual") +
    ggtitle("Distribution of Average Depth per Individual") +
    theme(axis.text.x = element_text(size = 14, angle = 45, vjust = 1, hjust = 1),
          axis.text.y = element_text(size = 14),
          axis.title.x = element_text(size = 16, face = "bold"),
          axis.title.y = element_text(size = 16, face = "bold"),
          plot.title = element_text(size = 18, face = "bold", hjust = 0.5),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black"),
          legend.position = "none")
}

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <species> <input_folder> <output_folder>")
}

species <- args[1]         # Not used, but still required
input_folder <- args[2]
output_folder <- args[3]

# List all CSV/TSV files in the input folder
files <- list.files(input_folder, pattern = "\\.csv$|\\.tsv$", full.names = TRUE)

if (length(files) == 0) {
  stop("No CSV/TSV files found in the specified input folder.")
}

# Read and label each file
df_list <- lapply(files, function(file) {
  df <- read.table(file, sep = ",", header = TRUE)
  
  # Extract individual name: everything before the first underscore
  individual_name <- strsplit(basename(file_path_sans_ext(file)), "_")[[1]][1]
  
  df$individual <- individual_name
  return(df)
})

# Combine all data
df_combined <- bind_rows(df_list)

# Generate violin plot
violin_plot <- plot_depth_coverage_violon(df_combined)

# Ensure output folder exists
if (!dir.exists(output_folder)) {
  dir.create(output_folder, recursive = TRUE)
  cat("Created output directory:", output_folder, "\n")
}

plot_name = paste0(species, "_violin_plot_avg_depth_individual_compare.png")

# Define output plot file path
output_plot_path <- file.path(output_folder, plot_name)

# Save plot
ggsave(output_plot_path, plot = violin_plot, width = 12, height = 6)

cat("Violin plot saved to:", output_plot_path, "\n")
