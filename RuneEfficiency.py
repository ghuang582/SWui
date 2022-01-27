import pandas as pd
import numpy as np
import re

max_stats = pd.read_csv(r"C:\Users\Admin\Desktop\SWOverlay\max_stats_table.csv")

# rune = [('DEF ', '+160 '), ('Accuracy ', '+7%'), ('CRI Dmg ', '+6%'), ('SPD ', '+24 '), ('HP ', '+12%')]
# rune = [('DEF ', '+160 '), ('ATK ', '+61'), ('CRI Rate ', '+17%'), ('CRI Dmg ', '6% '), ('HP ', '+363')]
# rune = [('DEF ', '+160 '), ('ATK ', '+19'), ('Accuracy ', '+4%'), ('CRI Rate ', '4% ')]
# rune_level = 0

def CalcEff(rune_list):
    rune = rune_list[1]
    rune_level = rune_list[0][0]
    # Trim white space from each entry
    rune = [[desc.strip() for desc in line] for line in rune]

    # Create dataframe and additional columns
    rune_df = pd.DataFrame(rune, columns = ["stat", "value"])

    rune_df['raw_value'] = rune_df['value'].str.replace(r"\D+", "", regex = True).astype('int')
    rune_df['type'] = np.where(rune_df['value'].str.find("%") > 0, "Percent", "Flat")

    # Join max_stats data on to rune dataframe
    rune_merged = pd.merge(rune_df, max_stats, on = ["stat", "type"], how = "left")

    # Calculate efficiency at a per stat level
    rune_merged['efficiency'] = rune_merged["raw_value"] / rune_merged["max"]

    # Halve the efficiency values of flat stats that aren't speed (SPD)
    rune_merged['efficiency'] = np.where((rune_merged['type'] == "Flat") & (rune_merged['stat'] != "SPD"), 0.5 * rune_merged['efficiency'], rune_merged['efficiency'])

    # Calculate total efficiency of rune
    total_eff = (1 + rune_merged['efficiency'][1:].sum()) / 2.8
    # print(total_eff)
    # print(rune_merged)

    # Calculate max efficiency of rune
    max_eff = total_eff + max((12 - rune_level)/3, 0) * 0.2 / 2.8
    # print(max_eff)

    return [total_eff, max_eff]
