##aDNA sequence length distribution plot##

#load libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(scales)  # for number formatting


plot_endogenous_reads <- function(species, source_file, target_folder) {
  
  print("Executing plot_endogenous_reads")
  
  # Read the source file
  df <- read.table(
    source_file, 
    sep =",", 
    header = FALSE, 
    col.names = c("protocol", "reads_total", "reads_endogenous", "percent_endogenous"))
  
  # Loop over each row of the dataframe
  for(i in 1:nrow(df)) {
    # Subset the row
    row_data <- df[i, ]
    
    # Create a long format for the row (pie chart data)
    row_long <- data.frame(
      read_type = c("reads_total", "reads_endogenous"),
      count = c(row_data$reads_total, row_data$reads_endogenous)
    )
    
    # Create the pie chart
    p <- ggplot(row_long, aes(x = "", y = count, fill = read_type)) +
      geom_bar(stat = "identity", width = 1) +
      coord_polar(theta = "y") +  # Create the pie chart by converting to polar coordinates
      scale_fill_manual(values = c("reads_total" = "#2ca02c",    # Blue
                                   "reads_endogenous" = "#ff7f0e")) +  # Orange
      labs(x = NULL, y = NULL, fill = "Read Type") +
      theme_void() +  # Remove background and axis labels
      theme(legend.position = "bottom")  # Place legend at the bottom
    
    # Create file name and path for each chart
    file_name <- paste0(row_data$protocol, "_endogenous_reads_pie_chart.png")
    file_path <- file.path(target_folder, file_name)
    
    # Save the plot
    ggsave(file_path, plot = p, width = 6, height = 6, dpi = 300)
  }
}



# FOR TESTING
plot_endogenous_reads(
  "Bger",
  "/Users/ssaadain/Documents/aDNA/Bger/results/endogenous_reads/Bger_endogenous_reads.csv",
  "/Users/ssaadain/Documents/aDNA/Bger/results/plots/endogenous_reads"
)


# Ensure you capture command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if the correct number of arguments are passed
if (length(args) < 3) {
  stop("Not enough arguments. Required: species, depth_file, target_folder.")
}

# Assign the arguments to variables
species <- args[1]
reads_analysis_file <- args[2]
target_folder <- args[3]

plot_endogenous_reads(
  species,
  reads_analysis_file,
  target_folder
)


