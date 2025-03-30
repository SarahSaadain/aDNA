library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)

process_and_plot_before_after <- function(root_folder, species_list, output_folder) {
  before_after_data <- list()
  
  for (species in species_list) {
    if (species == "Bger") {
      filepath <- file.path(root_folder, species, "results", "qualitycontrol", "processed_reads", paste0(species, "_reads_processing_result.tsv"))
      if (file.exists(filepath)) {
        df <- read.table(filepath, header = TRUE)
        Bger1_before_after <- df %>% filter(individual == "C1")
        Bger2_before_after <- df %>% filter(individual == "C2")
        Bger3_before_after <- df %>% filter(individual == "C3")
        
        Bger1_before_after$species <- "German cockroach Individual 1"
        Bger2_before_after$species <- "German cockroach Individual 2"
        Bger3_before_after$species <- "German cockroach Individual 3"
        
        before_after_data[["German cockroach Individual 1"]] <- Bger1_before_after
        before_after_data[["German cockroach Individual 2"]] <- Bger2_before_after
        before_after_data[["German cockroach Individual 3"]] <- Bger3_before_after
      } else {
        warning(paste("File not found:", filepath))
      }
    } else {
      filepath <- file.path(root_folder, species, "results", "qualitycontrol", "processed_reads", paste0(species, "_reads_processing_result.tsv"))
      if (file.exists(filepath)) {
        df <- read.table(filepath, header = TRUE)
        if(species == "trial_Dmel"){
          df$species <- "Drosophila melanogaster"
        } else if (species == "trial_Dsim"){
          df$species <- "trial Drosophila simulans"
        } else if (species == "trial_Phortica"){
          df$species <- "trial Phortica"
        } else if (species == "trial_Mmus"){
          df$species <- "trial House mouse"
        } else if (species == "trial_Sepsis"){
          df$species <- "trial Sepsis"
        } else if (species == "trial_Bger"){
          df$species <- "trial German cockroach"
        }
        
        before_after_data[[df$species[1]]] <- df
      } else {
        warning(paste("File not found:", filepath))
      }
    }
  }
  
  for (i in seq_along(before_after_data)){
    before_after_data[[i]]$protocol <- as.character(before_after_data[[i]]$protocol)
    if("individual" %in% colnames(before_after_data[[i]])){
      before_after_data[[i]]$individual <- as.character(before_after_data[[i]]$individual)
    }
  }
  
  df_before_after <- bind_rows(before_after_data)
  
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
  
  desired_order <- c("German cockroach Individual 1", "German cockroach Individual 2", "German cockroach Individual 3", "trial German cockroach", "trial Drosophila simulans", "Drosophila melanogaster", "trial Phortica", "trial House mouse", "trial Sepsis")
  df_long_species$species <- factor(df_long_species$species, levels = desired_order)
  
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
  
  ggsave(file.path(output_folder, paste0("plot_before_after_", paste(species_list, collapse = "_"), ".png")), plot_before_after, width = 12, height = 8, dpi = 300)
}


# Command line argument handling
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("Usage: Rscript script_name.R <root_folder> <species_list (comma-separated)> <output_folder>")
}

root_folder <- args[1]
species_list <- unlist(strsplit(args[2], ","))
output_folder <- args[3]

# Create the output directory if it doesn't exist
if (!dir.exists(output_folder)) {
  dir.create(output_folder, recursive = TRUE)
}

process_and_plot_before_after(root_folder, species_list, output_folder)
