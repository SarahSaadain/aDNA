library(ggplot2)
library(dplyr)
library(tools)

plot_coverage_breadth_violin <- function(df_breadth, individual) {
  df_breadth$individual <- individual

  plot_breadth <- ggplot(df_breadth, aes(x = factor(individual), y = percent_covered)) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Percent Covered") +
    xlab("Individual") +
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
          legend.position = "none")

  return(plot_breadth)
}

plot_coverage_breadth <- function(species, filepath, target_folder) {
  PLOT_BREADTH_VIOLIN <- cat(species, "_", "plot_breadth_violin_individual_compare.png")

  df <- read.table(filepath, sep = ",", header = TRUE)

  filename <- basename(file_path_sans_ext(filepath))
  individual <- strsplit(filename, "_")[[1]][1]

  if (!dir.exists(target_folder)) {
    dir.create(target_folder, recursive = TRUE)
    print(paste("Created directory:", target_folder))
  }

  if (!file.exists(file.path(target_folder, PLOT_BREADTH_VIOLIN))) {
    plot_violin <- plot_coverage_breadth_violin(df, individual)
    save_plot(plot_violin, target_folder, PLOT_BREADTH_VIOLIN)
    cat("Generating and saving plot:", PLOT_BREADTH_VIOLIN, "\n")
  } else {
    cat("File already exists, skipping plot generation:", PLOT_BREADTH_VIOLIN, "\n")
  }
}

save_plot <- function(plot, target_folder, file_name) {
  print(paste("Plotting", file_name, "to target folder:", target_folder))
  ggsave(file.path(target_folder, file_name), plot = plot, width = 10, height = 6)
}

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <species> <filepath> <target_folder>")
}

species <- args[1]
filepath <- args[2]
target_folder <- args[3]

plot_coverage_breadth(species, filepath, target_folder)
