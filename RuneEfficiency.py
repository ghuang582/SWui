import pandas as pd
import numpy as np
import re

max_stats = pd.read_csv(r"C:\Users\Admin\Desktop\SWOverlay\max_stats_table.csv")

rune = [('DEF ', '+160 '), ('Accuracy ', '+7%'), ('CRI Dmg ', '+6%'), ('SPD ', '+24 '), ('HP ', '+12%')]

# Trim white space from each entry
rune = [[desc.strip() for desc in line] for line in rune]

# Create dataframe and additional columns
rune_df = pd.DataFrame(rune, columns = ["stat", "value"])

rune_df['raw_value'] = rune_df['value'].str.replace(r"\D+", "", regex = True).astype('int')
rune_df['type'] = np.where(rune_df['value'].str.find("%") > 0, "Percent", "Flat")

# Join max_stats data onto rune dataframe
rune_merged = pd.merge(rune_df, max_stats, on = ["stat", "type"], how = "left")

# Calculate efficiency at a per stat level
rune_merged['efficiency'] = rune_merged["raw_value"] / rune_merged["max"]

# Calculate total efficiency of rune
print((1 + rune_merged['efficiency'][1:].sum()) / 2.8)
