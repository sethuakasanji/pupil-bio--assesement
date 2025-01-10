import pandas as pd
from scipy.stats import mannwhitneyu

# Step 1: Load the data
data = pd.read_csv("C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\Data Handling and Statostical Analysis\\Biomarker Identification\\grouped_output.csv")

# Step 2: Identify measurement columns (assume they are numeric columns starting from index 2)
measurement_columns = data.columns[2:-1]  # Exclude PMP, Tissue, and Sample_ID

# Step 3: Aggregate data: Calculate mean across measurement columns for each PMP and Tissue
aggregated_data = data.groupby(['PMP', 'Tissue'])[measurement_columns].mean().reset_index()

# Step 4: Perform Statistical Testing
# Separate data by tissue
cfDNA = aggregated_data[aggregated_data['Tissue'] == 'cfDNA']
islet = aggregated_data[aggregated_data['Tissue'] == 'Islet']

# Initialize results list
results = []

# Perform statistical testing for each PMP
for pmp in aggregated_data['PMP'].unique():
    cfDNA_values = cfDNA[cfDNA['PMP'] == pmp].iloc[:, 2:].values.flatten()
    islet_values = islet[islet['PMP'] == pmp].iloc[:, 2:].values.flatten()
    
    # Skip if data is missing for either tissue
    if len(cfDNA_values) == 0 or len(islet_values) == 0:
        continue
    
    # Mann-Whitney U test
    stat, p_value = mannwhitneyu(cfDNA_values, islet_values, alternative='two-sided')
    
    # Calculate threshold (mean of cfDNA as an example)
    threshold = cfDNA_values.mean()
    
    # Specificity: True Negatives / (True Negatives + False Positives)
    tn = sum(islet_values < threshold)
    fp = sum(islet_values >= threshold)
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # Sensitivity: True Positives / (True Positives + False Negatives)
    tp = sum(cfDNA_values >= threshold)
    fn = sum(cfDNA_values < threshold)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    # Store results
    results.append({
        'PMP': pmp,
        'p_value': p_value,
        'specificity': specificity,
        'sensitivity': sensitivity
    })

# Step 5: Filter High-Specificity PMPs
# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Filter PMPs based on thresholds
specific_pmps = results_df[
    (results_df['specificity'] > 0.9) &  # High specificity
    (results_df['p_value'] < 0.05) &    # Statistically significant
    (results_df['sensitivity'] > 0.5)  # Allow some false negatives
]

# Save the results
specific_pmps.to_csv("high_specificity_pmps.csv", index=False)
print(f"Total PMPs Selected: {len(specific_pmps)}")
print("High-specificity PMPs saved to 'high_specificity_pmps.csv'")