library(ggplot2)
library(dplyr)
library(readr)
library(tools)

plot_coverage_breadth_violoin <- function(df_breadth, species) {
  df_breadth$species <- species
  
  plot_breadth <- ggplot(all_data, aes(x = factor(species), y = percent_covered)) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Percent Covered") +
    xlab("Species") +
    ggtitle("Distribution of Percent Covered") +
    theme(axis.text.x = element_text(size = 18, angle = 45, vjust = 1, hjust = 1),
          legend.text = element_text(size = 18),
          axis.text.y = element_text(size = 18),
          axis.title.x = element_text(size = 20, face = "bold"),
          axis.title.y = element_text(size = 20, face = "bold"),
          plot.title = element_text(size = 24, face = "bold", hjust = 0.5),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black"),
          legend.position = "none") #+
    #scale_fill_manual(values = species_colors)

    return(plot_breadth)
}

plot_coverage_breadth <- function(species, filepath, target_folder) {
  # Read the TSV file into a data frame
  df <- read.table(
    filepath, 
    sep =",", 
    header = TRUE) # Changed to TRUE to read the header
  
  # Bin the scaffolds based on their length (total_bases)
  bins <- c(0, 100000, 250000, 500000, 1000000, 2500000, 5000000, 10000000, 20000000, Inf)  # Updated bins for scaffold length
  bin_labels <- c('0-100k', '100k-250k', '250k-500k', '500k-1M', '1M-2.5M', '2.5M-5M', '5M-10M', '10M-20M', '20M+')
  
  # Create a new column for the length bin
  df$length_bin <- cut(df$total_bases, breaks = bins, labels = bin_labels, right = FALSE)
  
  # Calculate the average percent_covered, count of scaffolds, and standard deviation for each bin
  avg_coverage_by_bin <- df %>%
    group_by(length_bin) %>%
    summarise(
      avg_coverage = mean(percent_covered, na.rm = TRUE),
      scaffold_count = n(),
      std_dev = sd(percent_covered, na.rm = TRUE)
    )
  
  # Extract the filename without extension
  filename <- file_path_sans_ext(basename(filepath))
  
  # Check if the target folder exists; if not, create it
  if (!dir.exists(target_folder)) {
    dir.create(target_folder, recursive = TRUE)
    print(paste("Created directory:", target_folder))
  }
  
  # Create the plot with error bars for standard deviation
  plot <- ggplot(avg_coverage_by_bin, aes(x = length_bin, y = avg_coverage, group = 1)) +
    geom_bar(stat = "identity", fill = "skyblue", color = "black") +
    geom_errorbar(aes(ymin = avg_coverage - std_dev, ymax = avg_coverage + std_dev), 
                  width = 0.2, color = "black") +  # Error bars for standard deviation
    labs(x = "Scaffold Length Bin", y = "Average Percent Covered", 
         title = paste("Average Coverage by Scaffold Length Bin:", filename)) +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate x-axis labels for better readability
  
  # Save the plot as a PNG file in the target folder
  output_filepath <- file.path(target_folder, paste0(filename, ".png"))
  ggsave(output_filepath, plot = plot, width = 10, height = 6)
  
  # Print message with the output path
  print(paste("Plot saved as:", output_filepath))
}

# Command-line arguments
args <- commandArgs(trailingOnly = TRUE)
species <- args[1]  # Species (not used in the plot but passed as an argument)
filepath <- args[2]  # Path to the input TSV file
target_folder <- args[3]  # Target folder for saving the plot

plot_coverage_breadth(species, filepath, target_folder)
