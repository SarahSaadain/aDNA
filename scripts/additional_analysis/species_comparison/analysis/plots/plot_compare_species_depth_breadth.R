library(dplyr)
library(ggplot2)
library(scales)
library(stringr)

process_and_plot_depth_breadth <- function(root_folder, species_list, output_folder) {
  depth_breadth_data <- list()
  
  for (species in species_list) {
    if (species == "Bger") {
      for (i in 1:3) {
        filepath <- file.path(root_folder, species, "results", "qualitycontrol", "depth_breadth", paste0("C", i, ".fastq_GCA_000762945.2_Bger_2.0_genomic_analysis.tsv"))
        if (file.exists(filepath)) {
          df <- read.table(filepath, header = TRUE)
          df$species <- paste("German cockroach Individual", i)
          depth_breadth_data[[paste("German cockroach Individual", i)]] <- df
        } else {
          warning(paste("File not found:", filepath))
        }
      }
    } else {
      filepath <- file.path(root_folder, species, "results", "qualitycontrol", "depth_breadth", paste0(str_match(list.files(file.path(root_folder, species, "results", "qualitycontrol", "depth_breadth")), ".*_genomic_analysis\\.tsv")[1,]))
      
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
        } else if (species == "trial_Bger"){
          df$species <- "trial German cockroach"
        }
        depth_breadth_data[[df$species[1]]] <- df
      } else {
        warning(paste("File not found:", filepath))
      }
    }
  }
  
  all_data <- bind_rows(depth_breadth_data)
  
  desired_order <- c("German cockroach Individual 1", "German cockroach Individual 2", "German cockroach Individual 3", "trial German cockroach", "trial Drosophila simulans", "Drosophila melanogaster", "trial Phortica", "trial House mouse")
  all_data$species <- factor(all_data$species, levels = desired_order)
  
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
  
  # Plot breadth
  plot_breadth <- ggplot(all_data, aes(x = factor(species), y = percent_covered, fill = species)) +
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
          legend.position = "none") +
    scale_fill_manual(values = species_colors)
  
  #print(plot_breadth)
  ggsave(file.path(output_folder, paste0("plot_breadth_", paste(species_list, collapse = "_"), ".png")), plot_breadth, width = 12, height = 8, dpi = 300)
  
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
          legend.position = "none") +
    scale_fill_manual(values = species_colors)
  
  ggsave(file.path(output_folder, paste0("plot_depth_", paste(species_list, collapse = "_"), ".png")), plot_depth, width = 12, height = 8, dpi = 300)
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

process_and_plot_depth_breadth(root_folder, species_list, output_folder)