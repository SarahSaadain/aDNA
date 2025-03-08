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
      read_type = c("Endogenous", "Non-Endogenous"),
      count = c(row_data$reads_endogenous, row_data$reads_total - row_data$reads_endogenous)
    )
 # Calculate percentages for labels
    row_long$percent <- row_long$count / sum(row_long$count) * 100

    # Create the pie chart
    p <- ggplot(row_long, aes(x = "", y = count, fill = read_type)) +
      geom_bar(stat = "identity", width = 1) +
      coord_polar(theta = "y") +  # Create the pie chart by converting to polar coordinates
      scale_fill_manual(values = c("Endogenous" = "#209557",  # Green
                             "Non-Endogenous" = "#1f5bb4")) + # Blue
      scale_y_continuous(labels = comma) +
      geom_text(aes(label = paste0(round(percent, 1), "%")), 
          position = position_stack(vjust = 0.5), 
          size = 6, color = "white") +  # Label with percentages
      labs(title = paste0("Protocol: ", row_data$protocol),
           subtitle = paste0("Total Reads: ", format(row_data$reads_total, big.mark = ",")), 
           fill = "Read Type") + # nolint: indentation_linter.
      theme_minimal(base_size = 14) +  # Set white background
      theme(legend.position = "bottom", 
            panel.grid = element_blank(),
            plot.title = element_text(hjust = 0.5, face = "bold"),
            plot.subtitle = element_text(hjust = 0.5))
            
    # Create file name and path for each chart
    file_name <- paste0(row_data$protocol, "_endogenous_reads_pie_chart.png")
    file_path <- file.path(target_folder, file_name)
    
    # Save the plot
ggsave(file_path, plot = p, width = 6, height = 6, dpi = 300, bg = "white")
  }
}



# FOR TESTING
#plot_endogenous_reads(
#  "Bger",
#  "/Users/ssaadain/Documents/aDNA/Bger/results/endogenous_reads/Bger_endogenous_reads.csv",
#  "/Users/ssaadain/Documents/aDNA/Bger/results/plots/endogenous_reads"
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


