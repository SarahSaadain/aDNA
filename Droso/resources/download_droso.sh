#!/bin/bash

USER="your_username"  # Replace with your username
PASS="your_password"  # Replace with your password

# Log file
LOGFILE="download_log_232V3GLT3.txt"

# List of download URLs
declare -a URLS=(
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_1_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_2_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_3_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_4_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_5_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_6_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_7_R19096_20250626.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/232V3GLT3_8_R19096_20250626.tar.gz"
)

# Download each file
for URL in "${URLS[@]}"; do
  FILE=$(basename "$URL")
  echo "[$(date)] Starting download of $FILE" | tee -a "$LOGFILE"

  wget -c --no-check-certificate --auth-no-challenge \
    --user "$USER" --password "$PASS" "$URL" >> "$LOGFILE" 2>&1

  echo "[$(date)] Finished $FILE" | tee -a "$LOGFILE"
  echo "----------------------------------------------" | tee -a "$LOGFILE"
done
