import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the data
file_path = "C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\PupilBioTest_PMP_revA.csv" 
df = pd.read_csv("C:\\Users\\mi161\\OneDrive\\Desktop\\Pupil Bio\\PupilBioTest_PMP_revA.csv")

# Renaming the column with backticks for easier access
df.rename(columns={"`000": "CpG_Coverage"}, inplace=True)

# Ensuring the CpG_Coverage column is numeric
df['CpG_Coverage'] = pd.to_numeric(df['CpG_Coverage'], errors='coerce')

# Calculating median and CV for each tissue
statistics = df.groupby('Tissue')['CpG_Coverage'].agg(['median', 'mean', 'std'])
statistics['CV'] = (statistics['std'] / statistics['mean']) * 100  
statistics = statistics[['median', 'CV']] 

# Printing statistics
print("CpG Coverage Statistics by Tissue:")
print(statistics)

# Enhanced histogram with KDE and median lines
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='CpG_Coverage', hue='Tissue', kde=True, bins=50, element='step', stat='density')

# Adding median lines for each tissue
for tissue in statistics.index:
    median = statistics.loc[tissue, 'median']
    plt.axvline(median, linestyle='--', label=f"{tissue} Median: {median:.2f}")

# Adding title, labels, and legend
plt.title("Enhanced CpG Coverage Histogram by Tissue with Median")
plt.xlabel("CpG Coverage")
plt.ylabel("Density")
plt.legend(title="Tissue")
plt.grid(axis='y')
plt.show()

# Box plot to summarize coverage statistics
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Tissue', y='CpG_Coverage')
plt.title("CpG Coverage Boxplot by Tissue")
plt.xlabel("Tissue")
plt.ylabel("CpG Coverage")
plt.grid(axis='y')
plt.show()

