#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Ensure data directories exist
data_dir = Path('data')
public_dir = data_dir / 'public'

if not data_dir.exists():
    data_dir.mkdir()
if not public_dir.exists():
    public_dir.mkdir()

print("Loading and merging raw data...")

# Load the four datasets
usagers_df = pd.read_csv(data_dir / "usagers-2023.csv", sep=';')
vehicules_df = pd.read_csv(data_dir / "vehicules-2023.csv", sep=';')
lieux_df = pd.read_csv(data_dir / "lieux-2023.csv", sep=';', low_memory=False)
caract_df = pd.read_csv(data_dir / "caract-2023.csv", sep=';')

# Start with usagers as the base dataframe (contains target 'grav')
df = usagers_df.copy()

# Merge with vehicles data
df = df.merge(vehicules_df, on=["Num_Acc", "id_vehicule"], how="left")

# Merge with location data
df = df.merge(lieux_df, on="Num_Acc", how="left")

# Merge with characteristics data
df = df.merge(caract_df, on="Num_Acc", how="left")

# Handle duplicate column names from merges
df = df.loc[:, ~df.columns.duplicated()]

print(f"Full merged dataset shape before filtering: {df.shape}")

# Remove rows with invalid 'grav' values (-1)
print(f"Number of rows with grav=-1: {(df['grav'] == -1).sum()}")
df = df[df['grav'].isin([1, 2, 3, 4])]
print(f"Dataset shape after filtering out invalid grav values: {df.shape}")

# First split: 80% private data, 20% public data
df_private, df_public = train_test_split(
    df, test_size=0.2, random_state=42, stratify=df['grav']
)

# Second split: split private data into train (80%) and test (20%)
df_private_train, df_private_test = train_test_split(
    df_private, test_size=0.2, random_state=42, stratify=df_private['grav']
)

# Third split: split public data into train (80%) and test (20%)
df_public_train, df_public_test = train_test_split(
    df_public, test_size=0.2, random_state=42, stratify=df_public['grav']
)

print(f"Private train dataset shape: {df_private_train.shape}")
print(f"Private test dataset shape: {df_private_test.shape}")
print(f"Public train dataset shape: {df_public_train.shape}")
print(f"Public test dataset shape: {df_public_test.shape}")

# Save all datasets
df_private_train.to_csv(data_dir / "train.csv", index=False)
df_private_test.to_csv(data_dir / "test.csv", index=False)
df_public_train.to_csv(public_dir / "train.csv", index=False)
df_public_test.to_csv(public_dir / "test.csv", index=False)

print("Data preparation complete. Files saved to data/ directory.") 