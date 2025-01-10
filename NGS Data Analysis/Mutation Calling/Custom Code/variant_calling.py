import subprocess
import os
import argparse

def run_command(command):
    """Helper function to run shell commands."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode()}")
    else:
        print(f"Command succeeded: {command}")
        print(result.stdout.decode())  # Print the output of the command

def check_file_exists(file_path):
    """Check if the file exists."""
    print(f"Checking file: {file_path}")  # Print the file path being checked
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return True

def call_variants(cancer_bam, normal_bam, reference_genome, output_vcf):
    """Call variants using bcftools."""
    # Check if the files exist
    check_file_exists(cancer_bam)
    check_file_exists(normal_bam)
    check_file_exists(reference_genome)
    
    # Variant calling with bcftools
    call_command = f"bcftools mpileup -f {reference_genome} {cancer_bam} {normal_bam} | bcftools call -mv -Ov -o {output_vcf}"
    run_command(call_command)

def filter_variants(input_vcf, output_vcf):
    """Filter variants using bcftools."""
    # Check if the input VCF file exists
    check_file_exists(input_vcf)
    
    filter_command = f"bcftools filter -e 'QUAL<20 || DP<10' {input_vcf} -Ov -o {output_vcf}"
    run_command(filter_command)

def compare_variants(cancer_vcf, normal_vcf, output_dir):
    """Compare VCF files to detect somatic mutations."""
    # Check if the VCF files exist
    check_file_exists(cancer_vcf)
    check_file_exists(normal_vcf)
    
    somatic_command = f"bcftools isec -n-1 -c all {cancer_vcf} {normal_vcf} -p {output_dir}"
    run_command(somatic_command)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Detect somatic mutations in cancer samples")
    parser.add_argument("--normal_bam", required=True, help="Path to the normal BAM file")
    parser.add_argument("--tumor_bam", required=True, help="Path to the tumor BAM file")
    parser.add_argument("--reference_genome", required=True, help="Path to the reference genome")
    parser.add_argument("--output_vcf", required=True, help="Path to save the output VCF file")
    parser.add_argument("--filtered_vcf", required=True, help="Path to save the filtered VCF file")
    parser.add_argument("--somatic_output", required=True, help="Directory to save somatic mutation results")
    
    args = parser.parse_args()
    
    # Step 1: Call variants
    print("Calling variants...")
    call_variants(args.tumor_bam, args.normal_bam, args.reference_genome, args.output_vcf)
    
    # Step 2: Filter variants
    print("Filtering variants...")
    filter_variants(args.output_vcf, args.filtered_vcf)
    
    # Step 3: Compare VCF files for somatic mutations
    print("Comparing VCF files for somatic mutations...")
    compare_variants(args.filtered_vcf, args.normal_bam, args.somatic_output)

if __name__ == "__main__":
    main()