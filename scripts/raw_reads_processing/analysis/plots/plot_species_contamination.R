## Kraken2 contamination boxplot ##

# Load required libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)

#------------------------------------------
# Function: Plot species counts as boxplots
#------------------------------------------
plot_kraken2_boxplot_by_species <- function(df, species, target_folder) {
  file_name <- paste0(species, "_kraken2_contamination_by_individual.png")
  file_path <- file.path(target_folder, file_name)

  # Skip plotting if the file already exists
  if (file.exists(file_path)) {
    message("Skipping Kraken2 boxplot: already exists at ", file_path)
    return()
  }

  # Convert wide format to long format
  df_long <- df %>%
    pivot_longer(
      cols = -individuum,             # All columns except 'individuum'
      names_to = "species_id",        # New column for species ID
      values_to = "count"             # Count values
    ) %>%
    mutate(species_id = as.factor(species_id))

  # Sort species by overall abundance (optional)
  species_order <- df_long %>%
    group_by(species_id) %>%
    summarise(total = sum(count)) %>%
    arrange(desc(total)) %>%
    pull(species_id)

  df_long$species_id <- factor(df_long$species_id, levels = species_order)

  # Create boxplot
  p <- ggplot(df_long, aes(x = species_id, y = count)) +
    geom_boxplot(fill = "steelblue", color = "black") +
    scale_y_continuous(labels = comma) +
    labs(
      title = paste("Kraken2 Species Count per Individuum -", species),
      x = "Species ID",
      y = "Read Count"
    ) +
    theme_bw() +
    theme(
      panel.grid.major = element_line(color = "grey90"),
      panel.grid.minor = element_blank(),
      axis.text.x = element_text(angle = 45, hjust = 1)
    )

  # Save plot
  ggsave(file_path, plot = p, width = 10, height = 6, dpi = 300)
  message("Saved Kraken2 boxplot to: ", file_path)
}

#------------------------------------------
# Master Function: Load data and call plot
#------------------------------------------
plot_kraken2_contamination_summary <- function(species, source_file, target_folder) {
  message("Running plot_kraken2_contamination_summary()")

  if (!file.exists(source_file)) {
    stop("Source file does not exist: ", source_file)
  }

  # Read input file (comma-separated)
  df <- read.csv(source_file, header = TRUE)

  # Check that individuum column exists
  if (!"individuum" %in% colnames(df)) {
    stop("Column 'individuum' not found in input file.")
  }

  # Generate plot
  plot_kraken2_boxplot_by_species(df, species, target_folder)
}

#------------------------------------------
# Main CLI execution
#------------------------------------------
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript plot_kraken2_species_boxplot.R <species> <input_file.csv> <output_folder>")
}

species <- args[1]
input_file <- args[2]
output_folder <- args[3]

plot_kraken2_contamination_summary(species, input_file, output_folder)
