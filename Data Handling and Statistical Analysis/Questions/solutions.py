import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the datasets
grouped_output = pd.read_csv("grouped_output.csv")
high_specificity_pmps = pd.read_csv("high_specificity_pmps.csv")
mean_vrf_results = pd.read_csv("mean_vrf_results.csv")

# === Sub-task 3(a): Sequencing Depth and Specificity Confidence === #
# Simulate sequencing depth
sequencing_depths = np.linspace(100000, 1000000, 10)  # From 100k to 1M reads
specificity_confidence = []

for depth in sequencing_depths:
    # Calculate confidence based on depth (hypothetical scaling of specificity)
    depth_confidence = high_specificity_pmps["specificity"] * (depth / 1000000)
    specificity_confidence.append(depth_confidence.mean())

# Plot specificity confidence vs sequencing depth
plt.figure(figsize=(8, 5))
plt.plot(sequencing_depths, specificity_confidence, marker='o', linestyle='-', color='blue')
plt.title("Effect of Sequencing Depth on Specificity Confidence")
plt.xlabel("Sequencing Depth (Reads)")
plt.ylabel("Specificity Confidence (Mean)")
plt.grid(True)
plt.show()




# === Sub-task 3(b): Threshold of Reads for Tissue #2 === #
# Calculate read threshold for Tissue #2
mean_vrf_results["Threshold_Reads"] = mean_vrf_results["VRF"] * 1_000_000

# Filter top 10 PMPs for Tissue #2
tissue_2_top_pmps = (
    mean_vrf_results[mean_vrf_results["Tissue"] == "Tissue #2"]
    .nlargest(10, "Threshold_Reads")
)
print("Top 10 PMPs with Threshold Reads for Tissue #2:")
print(tissue_2_top_pmps)



# === Sub-task 3(c): Validate Hypothesis === #
# Extract the top 10 PMPs based on specificity
top_10_pmps = high_specificity_pmps.nlargest(10, "specificity")

# Calculate average specificity for top PMPs
avg_specificity_pmps = top_10_pmps["specificity"].mean()

# Estimate specificity for individual CpG sites (average across methylation statuses)
individual_cpg_specificity = grouped_output.iloc[:, 2:10].mean(axis=1).mean()

# Compare the specificity
print(f"Average Specificity for Top 10 PMPs: {avg_specificity_pmps}")
print(f"Estimated Specificity for Individual CpG Sites: {individual_cpg_specificity}")

# Plot comparison
categories = ["Top 10 PMPs", "Individual CpG Sites"]
values = [avg_specificity_pmps, individual_cpg_specificity]

plt.figure(figsize=(8, 5))
plt.bar(categories, values, color=["green", "orange"])
plt.title("Specificity Comparison: Top 10 PMPs vs Individual CpG Sites")
plt.ylabel("Specificity")
plt.show()

