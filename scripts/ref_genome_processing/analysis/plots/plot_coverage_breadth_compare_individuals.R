library(ggplot2)
library(dplyr)
library(tools)

plot_coverage_breadth_violin <- function(df_combined) {
  ggplot(df_combined, aes(x = factor(individual), y = percent_covered)) +
    geom_violin(scale = "width") +
    theme_bw() +
    ylab("Percent Covered") +
    xlab("Individual") +
    ggtitle("Distribution of Percent Covered per Individual") +
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

save_plot <- function(plot, target_folder, file_name) {
  if (!dir.exists(target_folder)) {
    dir.create(target_folder, recursive = TRUE)
    cat("Created directory:", target_folder, "\n")
  }
  ggsave(file.path(target_folder, file_name), plot = plot, width = 12, height = 6)
}

plot_coverage_breadth <- function(species, input_folder, target_folder) {
  files <- list.files(input_folder, pattern = "\\.csv$|\\.tsv$", full.names = TRUE)

  if (length(files) == 0) {
    stop("No CSV/TSV files found in the specified input folder.")
  }

  df_list <- lapply(files, function(file) {
    df <- read.table(file, sep = ",", header = TRUE)
    
    if (nrow(df) == 0) {
      warning(paste("Skipped empty file:", file))
      return(NULL)
    }

    individual_name <- strsplit(basename(file_path_sans_ext(file)), "_")[[1]][1]
    df$individual <- individual_name
    return(df)
  })

# Remove any NULLs from the list
df_list <- Filter(Negate(is.null), df_list)

# Stop if no valid data was read
if (length(df_list) == 0) {
  stop("No valid non-empty CSV/TSV files found.")
}

  df_combined <- bind_rows(df_list)

  # Create violin plot for all individuals
  plot <- plot_coverage_breadth_violin(df_combined)
  plot_name <- paste0(species, "_plot_breadth_violin_all.png")

  save_plot(plot, target_folder, plot_name)
  cat("Saved combined violin plot to:", file.path(target_folder, plot_name), "\n")
}

# Command-line arguments
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <species> <input_folder> <target_folder>")
}

species <- args[1]
input_folder <- args[2]
target_folder <- args[3]

plot_coverage_breadth(species, input_folder, target_folder)
