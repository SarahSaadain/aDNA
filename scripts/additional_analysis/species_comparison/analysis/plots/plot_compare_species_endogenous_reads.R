#!/usr/bin/env Rscript

library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(stringr)
library(scales)

process_and_plot_endogenous_reads <- function(root_folder, species_list, output_folder) {
  # Initialize an empty list to store data frames
  endogenous_data <- list()
  
  # Iterate over each species in the species_list
  for (species in species_list) {
    # Construct the file path for the endogenous reads CSV file
    file_path <- file.path(root_folder, species, "results", "endogenous_reads", paste0(species, "_endogenous_reads.csv"))
    
    # Check if the file exists
    if (file.exists(file_path)) {
      # Read the CSV file
      df <- read.csv(file_path, header = FALSE)
      
      col_names <- c("sample", "endogenous", "total", "percent_endogenous")
      colnames(df) <- col_names
      
      # Handle specific rows for "Bger" species
      if (grepl("Bger", species)) {
        if (species == "Bger") {
          df1 <- df[3,]
          df2 <- df[1,]
          df3 <- df[2,]
          df1$species <- "Bger1"
          df2$species <- "Bger2"
          df3$species <- "Bger3"
          endogenous_data[[paste0(species,"1")]] <- df1
          endogenous_data[[paste0(species,"2")]] <- df2
          endogenous_data[[paste0(species,"3")]] <- df3
        } else {
          df <- df[1, ]
          df$species <- species
          endogenous_data[[species]] <- df
        }
      } else {
        # Select the first row for other species
        df <- df[1, ]
        df$species <- species
        endogenous_data[[species]] <- df
      }
    } else {
      # Print a warning if the file does not exist
      warning(paste("File not found:", file_path))
    }
  }
  
  # Combine all data frames into one data frame
  df_combined <- bind_rows(endogenous_data)
  
  # Assign column names

  
  # Create a new column combining species and sample name for x-axis labels
  df_combined$label <- paste(df_combined$species, df_combined$sample, sep = "_")
  
  # Convert percent_endogenous to percentage
  df_combined$percent_endogenous <- df_combined$percent_endogenous * 100
  
  # Recode species names for better readability in plots
  df_combined$species <- recode(df_combined$species,
                                Bger1 = "German cockroach Individual 1",
                                Bger2 = "German cockroach Individual 2",
                                Bger3 = "German cockroach Individual 3",
                                trial_Bger = "trial German cockroach",
                                trial_Mmus = "trial House mouse",
                                trial_Phortica = "trial Phortica",
                                trial_Dsim = "trial Drosophila simulans",
                                trial_Dmel = "Drosophila melanogaster"
  )
  
  # Define color palette for species
  species_colors <- c(
    "trial Drosophila simulans" = "salmon",
    "Drosophila melanogaster" = "orange",
    "trial German cockroach" = "chartreuse3",
    "German cockroach Individual 1" = "darkgreen",
    "German cockroach Individual 2" = "darkgreen",
    "German cockroach Individual 3" = "darkgreen",
    "trial House mouse" = "grey",
    "trial Phortica" = "darkorchid"
  )
  
  # Define desired order of species for plotting
  desired_order <- c("German cockroach Individual 1", "German cockroach Individual 2", "German cockroach Individual 3", "trial German cockroach", "trial Drosophila simulans", "Drosophila melanogaster", "trial Phortica", "trial House mouse")
  
  # Convert species column to factor with desired order
  df_combined$species <- factor(df_combined$species, levels = desired_order)
  
  # Reorder labels based on desired species order
  df_combined$label <- factor(df_combined$label, levels = df_combined$label[order(match(df_combined$species, desired_order))])
  
  # Create the plot
  endogenous_plot <- ggplot(df_combined, aes(x = species, y = percent_endogenous, fill = species)) +
    geom_bar(stat = "identity", position = "dodge") +
    theme_classic(base_size = 16) +
    labs(x = "Species", y = "Percentage of Endogenous Reads", title = "Endogenous Reads Across Species") +
    theme(axis.text.x = element_text(size = 14, angle = 45, vjust = 1, hjust = 1),
          axis.text.y = element_text(size = 16),
          axis.title.x = element_text(size = 18, face = "bold"),
          axis.title.y = element_text(size = 18, face = "bold"),
          plot.title = element_text(size = 22, face = "bold", hjust = 0.5),
          legend.position = "none",
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(),
          panel.background = element_rect(fill = "white", colour = "black")) +
    scale_fill_manual(values = species_colors) +
    scale_x_discrete(labels = c(
      "C2.fastq_GCA_000762945.2_Bger_2.0_genomic_sorted.bam" = "German Cockroach Individual 1",
      "C1.fastq_GCA_000762945.2_Bger_2.0_genomic_sorted.bam" = "German Cockroach Individual 2",
      "C3.fastq_GCA_000762945.2_Bger_2.0_genomic_sorted.bam" = "German Cockroach Individual 3",
      "German cockroach_trial_Bger_combined.fastq_GCA_000762945.2_Bger_2.0_genomic_sorted.bam" = "trial German Cockroach",
      "Drosophila simulans_trial_Dsim_combined.fastq_GCF_016746395.2_Prin_Dsim_3.1_genomic_sorted.bam" = "trial Drosophila simulans",
      "Drosophila melanogaster_trial_Dmel_combined.fastq_GCF_000001215.4_Release_6_plus_ISO1_MT_genomic_sorted.bam" = "Drosophila melanogaster",
      "Phortica_trial_Phortica_combined.fastq_GCA_001014415.1_ASM101441v1_genomic_sorted.bam" = "trial Phortica",
      "House mouse_trial_Mmus_combined.fastq_Mmus_ref_genome_sorted.bam" = "trial House mouse"
    ))
  
  # Print the plot
  #print(endogenous_plot)
  
  # Save the plot to the specified output folder
  ggsave(file.path(output_folder, paste0("plot_endogenous_reads_", paste(species_list, collapse = "_"), ".png")), endogenous_plot, width = 12, height = 8, dpi = 300)
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

# Call the function with command line arguments
process_and_plot_endogenous_reads(root_folder, species_list, output_folder)