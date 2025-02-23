##aDNA sequence length distribution plot##

#load libraries
library(dplyr)
library(ggplot2)
library(tidyr)


plot_sequence_length_distribution <- function(species, source_file, target_folder) {
  # Read the source file
  file <- read.table(source_file, header = TRUE)

  # Collapse 1 and 2
  file <- file %>%
    mutate(protocol_collapsed = gsub("[12]$", "", protocol))

  # Summarize read counts for each length and sample
  df_protocol <- file %>%
    group_by(protocol_collapsed) %>%
    summarise(raw_count_absolute = sum(raw_count),
              adapter_removed_count_absolute = sum(adapter_removed_count),
              duplicates_removed_count_absolute = sum(duplicates_removed_count),
              .groups = "drop")  # Count the number of reads for each length

  df_long <- df_protocol %>%
    pivot_longer(
      cols = c(raw_count_absolute, 
                adapter_removed_count_absolute,
                duplicates_removed_count_absolute),
      names_to = "read_type", values_to = "count"
    )

  df_long <- df_long %>%
    mutate(
      read_type = factor(
        read_type, levels = c("raw_count_absolute", 
                                "adapter_removed_count_absolute",
                                "duplicates_removed_count_absolute")))

  # Create the plot
  ggplot(df_long, aes(x = protocol_collapsed, y = count, fill = read_type)) +
    geom_bar(stat = "identity", position = position_dodge(preserve = "single")) +  # Ensures consistent grouping order
    scale_fill_manual(values = c("raw_count_absolute" = "#1f77b4",    # Blue
                                 "adapter_removed_count_absolute" = "#ff7f0e",  # Orange
                                 "duplicates_removed_count_absolute" = "#2ca02c")) +  # Green
    scale_y_continuous(labels = scales::comma) +  # Explicitly reference scales::comma
    labs(x = "Protocol", y = "Read Count", fill = "Read Type") +
    theme_bw() +  # Use a white background
    theme(panel.grid.major = element_line(color = "grey90"),  # Light grid lines
          panel.grid.minor = element_blank())

  file_name <- paste(species, "_sequence_length_distribution.png")
  file_path <- file.path(target_folder, file_name)

  # Save the plot
  ggsave(file_path, width = 8, height = 5, dpi = 300)
}


plot_sequence_length_distribution(
  "/Users/ssaadain/Documents/aDNA/Bger/results/processed_reads/Bger_reads_processing_result.tsv",
  "/Users/ssaadain/Documents/aDNA/Bger/results/plots/processed_reads/sequence_length_distribution.png"
)


# file <- read.table("/Users/ssaadain/Documents/aDNA/Bger/results/processed_reads/Bger_reads_processing_result.tsv", header = TRUE)

# #collapse 1 and 2
# file <- file %>%
#   mutate(protocol_collapsed = gsub("[12]$", "", protocol))

# # Summarize read counts for each length and sample
# df_protocol <- file %>%
#   group_by(protocol_collapsed) %>%
#   summarise(raw_count_absolute = sum(raw_count), adapter_removed_count_absolute = sum(adapter_removed_count), duplicates_removed_count_absolute = sum(duplicates_removed_count),.groups = 'drop')  # Count the number of reads for each length


# df_long <- df_protocol %>%
#   pivot_longer(cols = c(raw_count_absolute, adapter_removed_count_absolute, duplicates_removed_count_absolute),
#                names_to = "read_type", values_to = "count")


# df_long <- df_long %>%
#   mutate(read_type = factor(read_type, levels = c("raw_count_absolute", 
#                                                   "adapter_removed_count_absolute", 
#                                                   "duplicates_removed_count_absolute")))


# ggplot(df_long, aes(x = protocol_collapsed, y = count, fill = read_type)) +
#   geom_bar(stat = "identity", position = position_dodge(preserve = "single")) +  # Ensures consistent grouping order
#   scale_fill_manual(values = c("raw_count_absolute" = "#1f77b4",    # Blue
#                                "adapter_removed_count_absolute" = "#ff7f0e",  # Orange
#                                "duplicates_removed_count_absolute" = "#2ca02c")) +  # Green
#   scale_y_continuous(labels = scales::comma) +  # Explicitly reference scales::comma
#   labs(x = "Protocol", y = "Read Count", fill = "Read Type") +
#   theme_bw() +  # Use a white background
#   theme(panel.grid.major = element_line(color = "grey90"),  # Light grid lines
#         panel.grid.minor = element_blank()) 
# ggsave("/Users/ssaadain/Documents/aDNA/Bger/results/plots/processed_reads/sequence_length_distribution.png", width = 8, height = 5, dpi = 300)
