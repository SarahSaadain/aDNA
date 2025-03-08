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
    col.names = c("protocol", "reads_endogenous", "reads_total", "percent_endogenous"))
  
  # Add the Non-Endogenous reads and their percentages to the original dataframe
  df <- df %>%
    mutate(
      reads_non_endogenous = reads_total - reads_endogenous,  # Calculate Non-Endogenous reads
      percent_endogenous = percent_endogenous * 100, 
      percent_non_endogenous = (reads_non_endogenous / reads_total) * 100  # Calculate percentage
    )
  
  # Loop over each row of the dataframe
  for(i in 1:nrow(df)) {
    # Subset the row
    row_data <- df[i, ]
    
    # Create a long format for the row (pie chart data)
    row_long <- data.frame(
      read_type = c("Endogenous", "Non-Endogenous"),
      count = c(row_data$reads_endogenous, row_data$reads_non_endogenous),
      percent = c(row_data$percent_endogenous, row_data$percent_non_endogenous)
    )

    # Create the pie chart
    p <- ggplot(row_long, aes(x = "", y = count, fill = read_type)) +
      geom_bar(stat = "identity", width = 1) +
      coord_polar(theta = "y") +  # Create the pie chart by converting to polar coordinates
      geom_text(aes(label = paste0(round(percent, 1), "%")), 
                position = position_stack(vjust = 0.5), size = 5, color = "white") +
      scale_fill_manual(values = c("Endogenous" = "#209557",  # Green
                                  "Non-Endogenous" = "#1f5bb4")) + # Blue
      scale_y_continuous(labels = scales::comma) +
      labs(x = NULL, y = NULL, fill = "Read Type") +
      theme_bw() +
      theme(
        legend.position = "bottom"
      )

    # Create file name and path for each chart
    file_name <- paste0(row_data$protocol, "_endogenous_reads_pie_chart.png")
    file_path <- file.path(target_folder, file_name)
    
    # Save the plot
    ggsave(file_path, plot = p, width = 6, height = 6, dpi = 300)
  }
}

# FOR TESTING
#plot_endogenous_reads(
# "Bger",
# "/Users/ssaadain/Documents/aDNA/Bger/results/endogenous_reads/Bger_endogenous_reads.csv",
# "/Users/ssaadain/Documents/aDNA/Bger/results/plots/endogenous_reads"
#)


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


