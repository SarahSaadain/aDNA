library(tidyverse)
library(ggpubr)
library(dplyr)
library(purrr)
library(ggplot2)
library(tools)

plot_depth_coverage_violon <- function(df_depth, species) {

  df_depth$species <- species

  # Plot depth
  plot_depth_violin <- ggplot(df_depth, aes(x = factor(species), y = OverallAvgDepth)) +
    scale_y_continuous(
      trans = "log10",
      breaks = scales::trans_breaks("log10", function(x) 10^x),
      labels = scales::comma
    ) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Avg. Depth") +
    xlab("Species") +
    ggtitle("Distribution of Average Depth") +
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

    return(plot_depth_violin)
}

# Define the function
plot_depth_coverage <- function(depth, lengthScaffoldRange) {
  
  # Filter the data based on the scaffold length range
  depth_filtered <- depth %>%
    filter(OverallTotalBases >= lengthScaffoldRange[1] & OverallTotalBases <= lengthScaffoldRange[2])
  
  # Summarize the filtered data by average depth
  depth_filtered_mean <- depth_filtered %>%
    group_by(rounded_avg_depth) %>%
    summarise(nr_scaffolds = n(), .groups = "drop")
  
  # Create the plot
  plot_depth_coverage <- ggplot(depth_filtered_mean, aes(x = rounded_avg_depth, y = nr_scaffolds)) + 
    geom_line(color = "blue", size = 0.3) +  # Line for Mean Depth
    geom_point(color = "blue", size = 0.1) +  # Points for Mean Depth
    labs(title = paste("Depth Coverage of Scaffolds",  
                       " (Length range: ", 
                       format(lengthScaffoldRange[1], big.mark = ",", scientific = FALSE), 
                       " - ", format(lengthScaffoldRange[2], big.mark = ",", scientific = FALSE), ")", sep = ""),
         subtitle = paste(format(nrow(depth_filtered), big.mark = ",", scientific = FALSE), 
                          " of ", format(nrow(depth), big.mark = ",", scientific = FALSE), " Scaffolds", sep = ""),
         x = "Depth", y = "Number of Scaffolds") +
    scale_x_log10() +
    scale_y_log10() +
    theme_bw() +
    theme(legend.title = element_blank())

    return(plot_depth_coverage)
}

save_plot <- function(plot, target_folder, file_name){
  print(paste("Plotting", file_name, "to target folder:", target_folder))
  ggsave(file.path(target_folder, file_name), plot = plot, width = 10, height = 6)
}

# Define the function
plot_max_depth_coverage <- function(depth, lengthScaffoldRange) {
  
  # Filter based on bin size range
  depth_filtered <- depth[depth$OverallTotalBases >= lengthScaffoldRange[1] & depth$OverallTotalBases <= lengthScaffoldRange[2], ]
  
  depth_filtered_summary <- depth_filtered %>%
    group_by(rounded_max_depth) %>%
    summarise(nr_scaffolds=n())
  
  # Generate the plot
  depth_plot <- ggplot(depth_filtered_summary, aes(x = rounded_max_depth, y = nr_scaffolds)) +
    geom_line(size = 0.3) +  # Line for trend
    geom_point(size = 0.1) +   # Dots for individual points
    labs(title = paste(
      "Maximal Depth Coverage of Scaffolds",  
      " (Scaffold length from ",  
      format(lengthScaffoldRange[1], big.mark = ",", scientific = FALSE), 
      " - ", 
      format(lengthScaffoldRange[2], big.mark = ",", scientific = FALSE), 
      ")", 
      sep = ""), 
      subtitle = paste( 
        format(nrow(depth_filtered), big.mark = ",", scientific = FALSE), 
        " of ",
        format(nrow(depth), big.mark = ",", scientific = FALSE), 
        " Scaffolds",
        sep = ""), 
      x = "Maximum depth", y = "Number of Scaffolds") +
    scale_y_log10() +
    scale_x_log10() +
    theme_bw() +
    theme(legend.position = "none")
  
  # Return the plot
  return(depth_plot)
}

plot_coverage_depth <- function(species, depth_breath_analysis_file_path, target_folder){
  
  print("Executing plot_coverage_depth")
  
  # depth coverage for each scaffold
  df_depth <- read.table(
    depth_breath_analysis_file_path, 
    sep =",", 
    header = TRUE) # Changed to TRUE to read the header
  
  # Calculate the mean depth for each scaffold
  df_depth <- df_depth %>%
    mutate(
      rounded_avg_depth = round(OverallAvgDepth),
      rounded_max_depth = round(OverallMaxDepth)
    )
  
  max_length_of_scaffold <- max(df_depth$OverallTotalBases, na.rm = TRUE)

  plot_DepthCoverageOfAllScaffolds <- plot_depth_coverage(df_depth, c(0, max_length_of_scaffold))
  plot_DepthCoverageOfSuperSmallScaffolds <- plot_depth_coverage(df_depth, c(0, 1000) )
  plot_DepthCoverageOfSmallScaffolds <- plot_depth_coverage(df_depth, c(1001, 10000))
  plot_DepthCoverageOfMediumScaffolds <- plot_depth_coverage(df_depth, c(10001, 100000))
  plot_DepthCoverageOfLargeScaffolds <- plot_depth_coverage(df_depth, c(100001, max_length_of_scaffold))

  save_plot(plot_DepthCoverageOfAllScaffolds, target_folder, "plot_DepthCoverageOfAllScaffolds.png")
  save_plot(plot_DepthCoverageOfSuperSmallScaffolds, target_folder, "plot_DepthCoverageOfSuperSmallScaffolds.png")
  save_plot(plot_DepthCoverageOfSmallScaffolds, target_folder, "plot_DepthCoverageOfSmallScaffolds.png")
  save_plot(plot_DepthCoverageOfMediumScaffolds, target_folder, "plot_DepthCoverageOfMediumScaffolds.png")
  save_plot(plot_DepthCoverageOfLargeScaffolds, target_folder, "plot_DepthCoverageOfLargeScaffolds.png")  

  plot_MaxDepthCoverageOfAllScaffolds <- plot_max_depth_coverage(df_depth, c(0, max_length_of_scaffold))
  plot_MaxDepthCoverageOfSuperSmallScaffolds <- plot_max_depth_coverage(df_depth, c(0, 1000) )
  plot_MaxDepthCoverageOfSmallScaffolds <- plot_max_depth_coverage(df_depth, c(1001, 10000))
  plot_MaxDepthCoverageOfMediumScaffolds <- plot_max_depth_coverage(df_depth, c(10001, 100000))
  plot_MaxDepthCoverageOfLargeScaffolds <- plot_max_depth_coverage(df_depth, c(100001, max_length_of_scaffold))

  save_plot(plot_MaxDepthCoverageOfAllScaffolds, target_folder, "plot_MaxDepthCoverageOfAllScaffolds.png")
  save_plot(plot_MaxDepthCoverageOfSuperSmallScaffolds, target_folder, "plot_MaxDepthCoverageOfSuperSmallScaffolds.png")
  save_plot(plot_MaxDepthCoverageOfSmallScaffolds, target_folder, "plot_MaxDepthCoverageOfSmallScaffolds.png")
  save_plot(plot_MaxDepthCoverageOfMediumScaffolds, target_folder, "plot_MaxDepthCoverageOfMediumScaffolds.png")
  save_plot(plot_MaxDepthCoverageOfLargeScaffolds, target_folder, "plot_MaxDepthCoverageOfLargeScaffolds.png")

  plot_depth_violin <- plot_depth_coverage_violon(df_depth, species)
  save_plot(plot_depth_violin, target_folder, "plot_depthCoverage_violin.png")
  
}

# FOR TESTING
# plot_coverage_depth(
#   "Bger",
#   "/Users/ssaadain/Documents/aDNA/Bger/results/qualitycontrol/depth_breadth/C1.fastq_GCA_000762945.2_Bger_2.0_genomic_analysis.tsv",
#   "/Users/ssaadain/Documents/aDNA/Bger/results/plots/depth/C1.fastq_GCA_000762945.2_Bger_2.0_genomic"
# )

# Ensure you capture command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the correct number of arguments are passed
if (length(args) < 3) {
  stop("Not enough arguments. Required: species, depth_file, target_folder.")
}

# Assign the arguments to variables
species <- args[1]
depth_file <- args[2]
target_folder <- args[3]

plot_coverage_depth(
  species,
  depth_file,
  target_folder
)



