library(tidyverse)
library(ggpubr)
library(dplyr)
library(purrr)
library(ggplot2)

setwd("/Users/ssaadain/Documents/cockroach/aDNA/plots/Coverage/breadth/")

# breadth coverage for each scaffold
breadth <- read.table("breadth_coverage_mapBger2.txt", header = FALSE, 
                            col.names = c("scaffolds", "start", "end", "num_reads", "bases_covered", "bin_size", "coverage_fraction"))

max_length_of_scaffold <- max(breadth$bin_size, na.rm = TRUE)

breadth$percent_coverage <- round(breadth$coverage_fraction*100,0)

# Define the function
plot_breadth_coverage <- function(breadth, bin_size_range) {
  
  # Filter based on bin size range
  breadth_filtered <- breadth[breadth$bin_size >= bin_size_range[1] & breadth$bin_size <= bin_size_range[2], ]
  
  breadth_filtered_summary <- breadth_filtered %>%
    group_by(percent_coverage) %>%
    summarise(nr_scaffolds=n())
  
  # Generate the plot
  breadth_plot <- ggplot(breadth_filtered_summary, aes(x = percent_coverage, y = nr_scaffolds)) +
    geom_line(size = 0.3) +
    labs(title = paste(
            "Breadth Coverage of Scaffolds",  
            " (Scaffold length from ",  
            format(bin_size_range[1], big.mark = ",", scientific = FALSE), 
            " - ", 
            format(bin_size_range[2], big.mark = ",", scientific = FALSE), 
            ")", 
            sep = ""), 
         subtitle = paste( 
          format(nrow(breadth_filtered), big.mark = ",", scientific = FALSE), 
          " of ",
          format(nrow(breadth), big.mark = ",", scientific = FALSE), 
          " Scaffolds",
          sep = ""), 
         x = "breadth coverage in %", y = "number of scaffolds") +
    theme_bw() +
    theme(legend.position = "none")
  
  # Return the plot
  return(breadth_plot)
}

plot_BreadthCoverageOfAllScaffolds <- plot_breadth_coverage(breadth, c(0, max_length_of_scaffold))
plot_BreadthCoverageOfSuperSmallcaffolds <- plot_breadth_coverage(breadth, c(0, 1000) )
plot_BreadthCoverageOfSmallcaffolds <- plot_breadth_coverage(breadth, c(1001, 10000))
plot_BreadthCoverageOfMediumScaffolds <- plot_breadth_coverage(breadth, c(10001, 100000))
plot_BreadthCoverageOfLargeScaffolds <- plot_breadth_coverage(breadth, c(100001, max_length_of_scaffold))

ggsave("/Users/ssaadain/Documents/cockroach/aDNA/plots/Coverage/breadth/plot_BreadthCoverageOfAllScaffolds.png", plot = plot_BreadthCoverageOfAllScaffolds, width = 10, height = 6)
ggsave("/Users/ssaadain/Documents/cockroach/aDNA/plots/Coverage/breadth/plot_BreadthCoverageOfLargeScaffolds.png", plot = plot_BreadthCoverageOfLargeScaffolds, width = 10, height = 6)
ggsave("/Users/ssaadain/Documents/cockroach/aDNA/plots/Coverage/breadth/plot_BreadthCoverageOfMediumScaffolds.png", plot = plot_BreadthCoverageOfMediumScaffolds, width = 10, height = 6)
ggsave("/Users/ssaadain/Documents/cockroach/aDNA/plots/Coverage/breadth/plot_BreadthCoverageOfSmallScaffolds.png", plot = plot_BreadthCoverageOfSmallcaffolds, width = 10, height = 6)
ggsave("/Users/ssaadain/Documents/cockroach/aDNA/plots/Coverage/breadth/plot_BreadthCoverageOfSuperSmallcaffolds.png", plot = plot_BreadthCoverageOfSuperSmallcaffolds, width = 10, height = 6)

