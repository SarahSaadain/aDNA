#!/bin/bash

USER="your_username"  # Replace with your username
PASS="your_password"  # Replace with your password

# Log file
LOGFILE="download_log.txt"

# List of download URLs
declare -a URLS=(
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_1_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_2_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_3_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_4_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_5_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_6_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_7_R18987_20250612.tar.gz"
"https://ngs.vbcf.ac.at/api/tarfile/file/22TLJTLT4_8_R18987_20250612.tar.gz"
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