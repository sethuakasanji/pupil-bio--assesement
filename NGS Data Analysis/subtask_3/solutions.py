import numpy as np

# Paths to your R1 and R2 FASTA files (replace with actual file paths)
r1_file = "C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\normal_r1.fastq"
r2_file = "C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\normal_r2.fastq"

# Step 1: Function to parse a FASTA file and extract normal tissue mutations
def parse_fasta(file_path):
    mutations = []
    with open(file_path, 'r') as f:
        sequence = ''
        for line in f:
            line = line.strip()
            if line.startswith(">"):  # FASTA header line
                if sequence:
                    # Count mutations in the previous sequence (if it exists)
                    mutations.append(sequence.count('M'))  # 'M' represents a mutation
                sequence = ''
            else:
                # Append sequence data
                sequence += line
        if sequence:
            # Count mutations for the last sequence in the file
            mutations.append(sequence.count('M'))
    return mutations

# Step 2: Parse both R1 and R2 files
r1_mutations = parse_fasta(r1_file)
r2_mutations = parse_fasta(r2_file)

# Step 3: Combine mutations from both R1 and R2 (assuming they correspond to the same samples)
# This step may vary depending on how mutations are represented across R1 and R2.
normal_tissue_mutations = r1_mutations + r2_mutations

# Step 4: Calculate median background mutation level
median_background_mutation = np.median(normal_tissue_mutations)

# Step 5: Calculate RPM (Reads per Million)
total_reads = sum(normal_tissue_mutations)
rpm_values = [(mutation_count / total_reads) * 1_000_000 for mutation_count in normal_tissue_mutations]

# Step 6: Define mutation call threshold (e.g., 1.5x the median background mutation level)
mutation_threshold = median_background_mutation * 1.5

# Step 7: Output results
print(f"Median Background Mutation Level: {median_background_mutation}")
print(f"Total Reads: {total_reads}")
print(f"Mutation Call Threshold (1.5x Median): {mutation_threshold}")

# Print the RPM values and check if they exceed the threshold
for i, rpm in enumerate(rpm_values):
    print(f"Sample {i+1} RPM: {rpm}, Confident Call: {'Yes' if rpm > mutation_threshold else 'No'}")