
def process_input_file(input_file, output_dir):
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # create consensus fasta
    out_file_path = os.path.join(output_dir, f"{base_name}_consensus.fasta")
    print(f"Creating consensus sequence of {input_file}...")
    subprocess.run(["angsd", "-out", out_file_path, "-i", input_file, "-doFasta", "2", "-doCounts", "1"])