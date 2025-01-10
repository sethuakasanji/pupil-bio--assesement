#use this command in wsl ubuntu to extract VAF from VCF using bcftools 
#bcftools query -f '%INFO/AF\n' filtered_normal_variants.vcf > vaf_values.txt

import pandas as pd

# Load the GT values from the file
gt_file = 'gt_values.txt'

# Read the GT values into a pandas DataFrame
gt_data = pd.read_csv(gt_file, header=None, names=['GT'])

# Convert GT to VAF (0/1 -> 0.5, 1/1 -> 1.0)
vaf_data = gt_data['GT'].apply(lambda x: 0.5 if '0/1' in x else (1.0 if '1/1' in x else 0.0))

# Calculate the median VAF
median_vaf = vaf_data.median()
print(f'Median VAF in normal tissue: {median_vaf}')