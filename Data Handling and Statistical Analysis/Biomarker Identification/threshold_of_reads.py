import pandas as pd

# Step 1: Load the datasets
grouped_output = pd.read_csv("C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\Data Handling and Statostical Analysis\\Biomarker Identification\\grouped_output.csv")  # Replace with your file name
high_specificity_pmp = pd.read_csv("C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\Data Handling and Statostical Analysis\\Biomarker Identification\\high_specificity_pmps.csv")  # Replace with your file name

# Step 2: Select the top 10 PMPs based on specificity
top_10_pmps = high_specificity_pmp.sort_values("specificity", ascending=False).head(10)

# Step 3: Merge top 10 PMPs with grouped data to include sequencing depth
top_10_data = grouped_output.merge(top_10_pmps, on="PMP")

# Step 4: Filter for Tissue #2
tissue_2_data = top_10_data[top_10_data["Tissue2"] == "Tissue_2"]  # Replace "Tissue_2" with actual label

# Step 5: Normalize sequencing depth to 1 million reads
# Sum all numerical columns to represent sequencing depth
numerical_columns = tissue_2_data.select_dtypes(include=["int64", "float64"]).columns
tissue_2_data["total_depth"] = tissue_2_data[numerical_columns].sum(axis=1)
tissue_2_data["normalized_depth"] = (tissue_2_data["total_depth"] / tissue_2_data["total_depth"].sum()) * 1_000_000

# Step 6: Calculate read threshold
# Assuming a confidence threshold (e.g., 95% specificity)
confidence_threshold = 0.95
tissue_2_data["read_threshold"] = tissue_2_data["normalized_depth"] * confidence_threshold

# Step 7: Display results
print("Top 10 PMPs and their read thresholds for Tissue #2:")
print(tissue_2_data[["PMP", "specificity", "normalized_depth", "read_threshold"]])

# Optional: Save the results to a CSV
tissue_2_data[["PMP", "specificity", "normalized_depth", "read_threshold"]].to_csv("top_10_pmp_read_thresholds.csv", index=False)

print("Results saved to 'top_10_pmp_read_thresholds.csv'.")