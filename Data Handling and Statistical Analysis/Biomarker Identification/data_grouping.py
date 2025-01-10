import pandas as pd

# Load the data
file_path = "C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\PupilBioTest_PMP_revA.csv"  # Replace with your file path
df = pd.read_csv("C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\PupilBioTest_PMP_revA.csv")

# Inspect column names
print("Columns in the dataset:", df.columns.tolist())

# Define PMP using strand and CpG_Coordinates
df['PMP'] = df['strand'] + '_' + df['CpG_Coordinates']

# Group by PMP and Tissue, and aggregate counts for numerical columns
numerical_columns = df.select_dtypes(include='number').columns.tolist()
grouped = df.groupby(['PMP', 'Tissue'])[numerical_columns].sum().reset_index()

# Display the first few rows of the grouped data
print("Grouped Data:")
print(grouped.head())

# Save the output to a new file
output_path = "grouped_output.csv"  # Replace with your desired output file path
grouped.to_csv(output_path, index=False)
print(f"Grouped data saved to: {output_path}")