import pandas as pd
import numpy as np

# Load the processed output dataset
final_df = pd.read_csv("final_output.csv")

# Replace zero or missing income values to safely compute logarithms
final_df['total_household_income'] = final_df['total_household_income'].replace(0, np.nan)

# Compute log of total household income
final_df['log_income'] = np.log(final_df['total_household_income'])

# Group by age of household head (m1ac5) and compute the average log income
# Since the dataset only contains household heads, one row per household
gt_df = final_df.groupby('m1ac5')['log_income'].mean().reset_index()
gt_df.columns = ['age', 'avg_log_income']

# Exponentiate average log income to get G_t
gt_df['G_t'] = np.exp(gt_df['avg_log_income'])

# Save the resulting G_t values to a CSV file
gt_df.to_csv("G_t_new.csv")

# Print entire G_t table to the terminal
print("\nG_t table by age:")
print(gt_df.to_string(index=False))
print("\n✅ G_t table saved to 'gt_by_age.csv'")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(gt_df['age'], gt_df['G_t'], marker='o', linestyle='-')
plt.title('Geometric Mean Household Income (Gₜ) by Age of Household Head')
plt.xlabel('Age')
plt.ylabel('Gₜ (Geometric Mean Income)')
plt.grid(True)
plt.tight_layout()
plt.savefig("gt_by_age_plot.png")
plt.show()
