# MD5
## Expected MD5

| File                                 | Expected MD5                       |
| ------------------------------------ | ---------------------------------- |
| `22TLJTLT4_1_R18987_20250612.tar.gz` | `20c32fbb97af170fb1a43ecbfcaa0f69` |
| `22TLJTLT4_2_R18987_20250612.tar.gz` | `8bf3e6e02ce710c5091d8b7f014ad540` |
| `22TLJTLT4_3_R18987_20250612.tar.gz` | `8f91beda9e7f305682de5e20660dc48d` |
| `22TLJTLT4_4_R18987_20250612.tar.gz` | `2485e39702d89ffb3dff7f702c78152e` |
| `22TLJTLT4_5_R18987_20250612.tar.gz` | `77ad7c2c7f5f888c2a329dea1f0f4281` |
| `22TLJTLT4_6_R18987_20250612.tar.gz` | `87cfbdc15a0f15d4c795ef206a235d4f` |
| `22TLJTLT4_7_R18987_20250612.tar.gz` | `8c4d437078a44e5b50430e976039835f` |
| `22TLJTLT4_8_R18987_20250612.tar.gz` | `d2833805841f8dba565305e378d5dd65` |

## MD5 Check

```bash
nohup sh -c 'md5sum 22TLJTLT4_*_R18987_20250612.tar.gz > md5sums.txt' &> md5sum.log &

nohup sh -c 'md5sum 22TLJTLT4_1_R18987_20250612.tar.gz > md5sum_1.txt' &> md5sum_1.log &
nohup sh -c 'md5sum 22TLJTLT4_2_R18987_20250612.tar.gz > md5sum_2.txt' &> md5sum_2.log &
nohup sh -c 'md5sum 22TLJTLT4_3_R18987_20250612.tar.gz > md5sum_3.txt' &> md5sum_3.log &
nohup sh -c 'md5sum 22TLJTLT4_4_R18987_20250612.tar.gz > md5sum_4.txt' &> md5sum_4.log &
nohup sh -c 'md5sum 22TLJTLT4_5_R18987_20250612.tar.gz > md5sum_5.txt' &> md5sum_5.log &
nohup sh -c 'md5sum 22TLJTLT4_6_R18987_20250612.tar.gz > md5sum_6.txt' &> md5sum_6.log &
nohup sh -c 'md5sum 22TLJTLT4_7_R18987_20250612.tar.gz > md5sum_7.txt' &> md5sum_7.log &
nohup sh -c 'md5sum 22TLJTLT4_8_R18987_20250612.tar.gz > md5sum_8.txt' &> md5sum_8.log &
```

Check if running:

ps aux | grep md5sum

# Unzip

```bash
nohup tar -xvzf 22TLJTLT4_1_R18987_20250612.tar.gz > extract_1.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_2_R18987_20250612.tar.gz > extract_2.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_3_R18987_20250612.tar.gz > extract_3.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_4_R18987_20250612.tar.gz > extract_4.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_5_R18987_20250612.tar.gz > extract_5.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_6_R18987_20250612.tar.gz > extract_6.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_7_R18987_20250612.tar.gz > extract_7.log 2>&1 &
nohup tar -xvzf 22TLJTLT4_8_R18987_20250612.tar.gz > extract_8.log 2>&1 &
```