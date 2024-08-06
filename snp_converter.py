import argparse
import logging
import os
from datetime import datetime
import pysam

def parse_args():
    parser = argparse.ArgumentParser(description="Convert SNP format to REF/ALT format")
    parser.add_argument("-i", "--input", required=True, help="Input file path")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("-f", "--fasta", required=True, help="Directory containing reference FASTA files")
    parser.add_argument("-l", "--log", required=True, help="Log file path")
    return parser.parse_args()

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging is set up.")

def get_ref_allele(chrom, pos, fasta_dir):
    fasta_file = os.path.join(fasta_dir, f"{chrom}.fa")
    if not os.path.exists(fasta_file):
        raise FileNotFoundError(f"FASTA file {fasta_file} not found.")
    fasta = pysam.FastaFile(fasta_file)
    ref_allele = fasta.fetch(f"{chrom}", pos-1, pos)
    return ref_allele

def convert_snp_format(input_file, output_file, fasta_dir):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        header = infile.readline().strip().split('\t')
        if header != ["#CHROM", "POS", "ID", "allele1", "allele2"]:
            raise ValueError("Input file has incorrect header.")
        
        outfile.write("#CHROM\tPOS\tID\tREF\tALT\tNOTE\n")
        
        for line in infile:
            chrom, pos, snp_id, allele1, allele2 = line.strip().split('\t')
            pos = int(pos)
            
            ref_allele = get_ref_allele(chrom, pos, fasta_dir)
            if ref_allele == allele1:
                alt_allele = allele2
                note = ""
            elif ref_allele == allele2:
                alt_allele = allele1
                note = ""
            else:
                logging.warning(f"Neither allele matches reference for SNP {snp_id} at {chrom}:{pos}")
                ref_allele = allele1  # Assuming allele1 as REF in such cases
                alt_allele = allele2  # Assuming allele2 as ALT in such cases
                note = "Neither allele matches reference"
            
            outfile.write(f"{chrom}\t{pos}\t{snp_id}\t{ref_allele}\t{alt_allele}\t{note}\n")
            logging.info(f"Processed SNP {snp_id} at {chrom}:{pos}")

def main():
    args = parse_args()
    setup_logging(args.log)
    
    logging.info("Starting conversion process.")
    try:
        convert_snp_format(args.input, args.output, args.fasta)
        logging.info("Conversion completed successfully.")
    except Exception as e:
        logging.error(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
    
    
    
print("Checking file paths:")
print(f"Input file: {os.path.abspath('/app/data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv')}")
print(f"Reference dir: {os.path.abspath('/app/ref/GRCh38.d1.vd1_mainChr/sepChrs')}")