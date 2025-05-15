import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("muc123a.csv")

print(df)
#Filter to group people in the same household
household_cols = ['tinh', 'huyen', 'xa', 'diaban', 'hoso']
df['family_size'] = df.groupby(household_cols)['matv'].transform('max')

#Save or display the result
print(df[['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'family_size']])

# Step: Load income data
income_df = pd.read_csv("muc4a.csv")

# Step: Calculate individual income
income_cols = ['m4ac11', 'm4ac12f', 'm4ac21', 'm4ac22f', 'm4ac25']
income_df['individual_income'] = income_df[income_cols].sum(axis=1)

# Step: Merge income into the main df using household keys + matv
keys = ['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv']
df = pd.merge(df, income_df[['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv', 'individual_income']],
              on=keys, how='left')

# Compute total household income
df['total_household_income'] = df.groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['individual_income'].transform('sum')
3

df = df[df['m1ac3'] == 1]
df = df[df['m1ac2'] == 1]
df = df[df['m1ac5'] >= 25]

# Load consumption  data
consumption_df = pd.read_csv("muc5a1.csv", delimiter=';')
keys2 = ['tinh', 'huyen', 'xa', 'diaban', 'hoso']
#  Sum total household consumption 
consumption_sum = (
    consumption_df
    .groupby(keys2)['m5a1c2b']
    .sum()
    .reset_index()
    .rename(columns={'m5a1c2b': 'consumption'})
)
#  Sum consumption 2
consumption2_sum = (
    consumption_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['m5a1c3b']
    .sum()
    .reset_index()
    .rename(columns={'m5a1c3b': 'consumption 2'})
)

# Combine both consumption summaries
consumption_all = pd.merge(
    consumption_sum,
    consumption2_sum,
    on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'],
    how='outer'
)
# merge into df (after income and household filters)
df = pd.merge(df, consumption_all, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='left')

# Step: Load dataset for consumption 3
consumption3_df = pd.read_csv("muc5a2.csv", delimiter=';')

# Step: Calculate consumption 3
consumption3_df['consumption 3'] = consumption3_df[['m5a2c6', 'm5a2c10']].sum(axis=1)

# Step: Group and sum 'consumption 3' by household
consumption3_sum = (
    consumption3_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['consumption 3']
    .sum()
    .reset_index()
)
# Step: Merge into main df
df = pd.merge(df,consumption3_sum, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='left')

# Step: Load consumption 4 dataset
consumption4_df = pd.read_csv("muc5b1.csv", delimiter=',')
consumption4_df

# Step: Calculate consumption 4
consumption4_df['consumption 4'] = consumption4_df['m5b1c4']+consumption4_df['m5b1c5']

# Group and sum consumption 4 by household
consumption4_sum = (
    consumption4_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['consumption 4']
    .sum()
    .reset_index()
)
# Merge into main df
df = pd.merge(df, consumption4_sum, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='left')

# Step: Load consumption 5 dataset
consumption5_df = pd.read_csv("muc5b2.csv", delimiter=',')

# Step: Calculate consumption 5
consumption5_df['consumption 5'] = consumption5_df[['m5b2c2', 'm5b2c3']].sum(axis=1)

# Group and sum consumption 5 by household
consumption5_sum = (
    consumption5_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['consumption 5']
    .sum()
    .reset_index()
)

# Merge into main df
df = pd.merge(df, consumption5_sum, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='left')

# Step: Load consumption 6 dataset
consumption6_df = pd.read_csv("muc5b3.csv", delimiter = ',')

# Step: Calculate consumption 6 from m5b3c2
consumption6_df['consumption 6'] = consumption6_df['m5b3c2']

# Group and sum consumption 6 by household
consumption6_sum = (
    consumption6_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['consumption 6']
    .sum()
    .reset_index()
)

# Merge into main df
df = pd.merge(df, consumption6_sum, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='left')

# Load
consumption7_df = pd.read_csv("muc7.csv", delimiter=';')

# Check actual columns (optional)
print(consumption7_df.columns.tolist())

# Calculate consumption 7 safely
cols_7 = ['m7c32', 'm7c36', 'm7c39']  # Confirm after printing above
consumption7_df['consumption 7'] = consumption7_df[cols_7].sum(axis=1)

# Group by household
consumption7_sum = (
    consumption7_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'])['consumption 7']
    .sum()
    .reset_index()
)

# Merge
df = pd.merge(df, consumption7_sum, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='left')

#compute total consumption
df['total consumption'] = df[[
    'consumption', 'consumption 2', 'consumption 3',
    'consumption 4', 'consumption 5', 'consumption 6', 'consumption 7'
]].sum(axis=1)

df['avr_consumption'] = df['total consumption'] / df['family_size']

# Load fixed and durable asset data 
fixed_assets_df = pd.read_csv("muc6a.csv", delimiter = ',')
durable_assets_df = pd.read_csv("muc6b.csv", delimiter = ',')

# Calculate fixed asset wealth 
for col in ['m6ac3', 'm6ac6', 'm6ac7']:
    fixed_assets_df[col] = pd.to_numeric(fixed_assets_df[col], errors='coerce')

fixed_assets_df['wealth_fixed'] = (
    fixed_assets_df['m6ac3'] * fixed_assets_df['m6ac6'] * (fixed_assets_df['m6ac7'] / 100)
)

# Group fixed asset wealth by household
fixed_wealth_sum = (
    fixed_assets_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'], as_index=False)['wealth_fixed']
    .sum()
)

# Calculate durable appliance wealth 
for col in ['m6bc3', 'm6bc6']:
    durable_assets_df[col] = pd.to_numeric(durable_assets_df[col], errors='coerce')

durable_assets_df['wealth_durable'] = (
    durable_assets_df['m6bc3'] * durable_assets_df['m6bc6']
)

# Group durable wealth by household
durable_wealth_sum = (
    durable_assets_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'], as_index=False)['wealth_durable']
    .sum()
)

# Merge fixed assets and durable appliances wealth 
wealth_df = pd.merge(
    fixed_wealth_sum,
    durable_wealth_sum,
    on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'],
    how='outer'
)

# Fill missing values with 0 to calculate total wealth
wealth_df[['wealth_fixed', 'wealth_durable']] = wealth_df[['wealth_fixed', 'wealth_durable']].fillna(0)
wealth_df['total_wealth'] = wealth_df['wealth_fixed'] + wealth_df['wealth_durable']

# Merge into the main df ===
df = pd.merge(
    df,
    wealth_df,
    on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'],
    how='left'
)

# Ensure working hours columns are numeric
for col in ['m4ac6', 'm4ac7', 'm4ac8', 'm4ac16', 'm4ac17', 'm4ac18']:
    income_df[col] = pd.to_numeric(income_df[col], errors='coerce')

# Compute individual total working hours
income_df['main_job_hours'] = income_df['m4ac6'] * income_df['m4ac7'] * income_df['m4ac8']
income_df['secondary_job_hours'] = income_df['m4ac16'] * income_df['m4ac17'] * income_df['m4ac18']
income_df['total_working_hours'] = income_df['main_job_hours'].fillna(0) + income_df['secondary_job_hours'].fillna(0)

# Merge household income into income_df to allow filtering
income_df = pd.merge(
    income_df,
    df[['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'total_household_income']].drop_duplicates(),
    on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'],
    how='left'
)

# Filter to valid households (income > 0)
income_df = income_df[income_df['total_household_income'] > 0]

# Compute household-level stats
working_stats = (
    income_df
    .groupby(['tinh', 'huyen', 'xa', 'diaban', 'hoso'], as_index=False)
    .agg(
        households_working_hours=('total_working_hours', 'sum'),
        num_workers=('total_working_hours', lambda x: (x > 0).sum())
    )
)

# Average per worker
working_stats['avg_working_hours_per_worker'] = (
    working_stats['households_working_hours'] / working_stats['num_workers']
)

# Merge into the main df
df = pd.merge(df, working_stats, on=['tinh', 'huyen', 'xa', 'diaban', 'hoso'], how='inner')

# Load the processed dataset
df = pd.read_csv("final_output.csv")

# Drop rows with missing values in the two relevant columns
df_clean = df[['households_working_hours', 'total consumption']].dropna()

# Extract x and y
x = df_clean['households_working_hours'].values
y = df_clean['total consumption'].values

# Fit a linear regression line
coeffs = np.polyfit(x, y, deg=1)
reg_line = np.poly1d(coeffs)

# Generate points for the regression line
x_line = np.linspace(x.min(), x.max(), 100)
y_line = reg_line(x_line)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='darkgreen', alpha=0.6, label='Data')
plt.plot(x_line, y_line, color='red', linewidth=2, label='Fitted Line')

plt.title('Household Consumption vs. Working Hours')
plt.xlabel('Households Working Hours')
plt.ylabel('Total Household Consumption')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Final Display 
print(df[['tinh', 'huyen', 'xa', 'diaban', 'hoso', 'matv',
          'family_size', 'total_household_income',
          'consumption', 'consumption 2', 'consumption 3',
          'consumption 4', 'consumption 5', 'consumption 6', 'consumption 7',
          'total consumption', 'avr_consumption',
          'wealth_fixed', 'wealth_durable', 'total_wealth',
          'households_working_hours', 'avg_working_hours_per_worker']])

df = df.rename(columns={'m1ac5': 'age'})

# Save to file
df.to_csv("final_output.csv", index=False)

