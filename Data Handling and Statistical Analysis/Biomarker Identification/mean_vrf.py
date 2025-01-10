import pandas as pd

# Load the grouped dataset
grouped_file_path = "C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\Data Handling and Statostical Analysis\\Biomarker Identification\\grouped_output.csv"  # Update with your file path
data = pd.read_csv("C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\Data Handling and Statostical Analysis\\Biomarker Identification\\grouped_output.csv")

# Calculate total read counts for each row (excluding PMP and Tissue columns)
data['Total_Reads'] = data.iloc[:, 2:].sum(axis=1)

# Calculate VRF for each row
data['VRF'] = data['Total_Reads'] / data['Total_Reads'].sum()

# Group by PMP and Tissue to calculate the mean VRF
mean_vrf = data.groupby(['PMP', 'Tissue'])['VRF'].mean().reset_index()

# Save the result to a CSV file
output_path = "mean_vrf_results.csv"
mean_vrf.to_csv(output_path, index=False)

print(f"Mean VRF calculated and saved to {output_path}")