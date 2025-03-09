#!/usr/bin/env python3

import os
import urllib.request
import ssl
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


def download_file(url, output_file, context):
    """
    Download a file from a URL and save it to the specified path
    """
    try:
        with urllib.request.urlopen(url, context=context) as response:
            data = response.read()

            with open(output_file, 'wb') as file:
                file.write(data)
            print("Successfully downloaded to", output_file)
            return True
    except Exception as e:
        print(f"Error downloading {output_file}: {e}", file=sys.stderr)
        print("\nTry downloading manually:")
        print(f"curl -o {output_file} '{url}'")
        return False


def read_csv_safely(file_path):
    """
    Read a CSV file with different encodings and separators
    """
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    separators = [',', ';']

    for encoding in encodings:
        for sep in separators:
            try:
                return pd.read_csv(
                    file_path,
                    encoding=encoding,
                    sep=sep,
                    low_memory=False
                )
            except Exception:
                continue

    raise ValueError(
        f"Could not read {file_path} with any combination of "
        "encoding and separator"
    )


def download_data():
    """
    Download the CSV files from data.gouv.fr website
    """
    # Create data directory if it doesn't exist
    data_dir = Path('data')
    if not data_dir.exists():
        data_dir.mkdir()

    # URLs and filenames for the different datasets
    base_url = "https://www.data.gouv.fr/fr/datasets/r"
    datasets = {
        'usagers': {
            'url': f"{base_url}/68848e2a-28dd-4efc-9d5f-d512f7dbe66f",
            'filename': "usagers-2023.csv"
        },
        'vehicules': {
            'url': f"{base_url}/146a42f5-19f0-4b3e-a887-5cd8fbef057b",
            'filename': "vehicules-2023.csv"
        },
        'lieux': {
            'url': f"{base_url}/8bef19bf-a5e4-46b3-b5f9-a145da4686bc",
            'filename': "lieux-2023.csv"
        },
        'caracteristiques': {
            'url': f"{base_url}/104dbb32-704f-4e99-a71e-43563cb604f2",
            'filename': "caract-2023.csv"
        }
    }

    # Create SSL context that ignores certificate verification
    context = ssl._create_unverified_context()

    # Download all files
    _ = True
    downloaded_files = []

    for dataset_type, info in datasets.items():
        output_file = os.path.join(data_dir, info['filename'])

        # Only download if the file doesn't exist
        if not os.path.exists(output_file):
            print(f"\nDownloading {dataset_type} data...")
            print(f"URL: {info['url']}")

            if download_file(info['url'], output_file, context):
                downloaded_files.append(output_file)
            else:
                _ = False
        else:
            print(f"\nFile {output_file} already exists, skipping download.")
            downloaded_files.append(output_file)

    return downloaded_files


def prepare_data(data_files):
    """
    Prepare the data by merging datasets, filtering invalid values,
    and creating train/test splits for both public and private data.
    """
    print("\nPreparing data...")

    # Ensure public directory exists
    data_dir = Path('data')
    public_dir = data_dir / 'public'
    if not public_dir.exists():
        public_dir.mkdir()

    # Load the four datasets
    print("Loading datasets...")
    usagers_df = pd.read_csv(data_dir / "usagers-2023.csv", sep=';')
    vehicules_df = pd.read_csv(data_dir / "vehicules-2023.csv", sep=';')
    lieux_df = pd.read_csv(
        data_dir / "lieux-2023.csv",
        sep=';',
        low_memory=False
    )
    caract_df = pd.read_csv(data_dir / "caract-2023.csv", sep=';')

    # Start with usagers as the base dataframe (contains target 'grav')
    print("Merging datasets...")
    df = usagers_df.copy()

    # Merge with vehicles data
    df = df.merge(vehicules_df, on=["Num_Acc", "id_vehicule"], how="left")

    # Merge with location data
    df = df.merge(lieux_df, on="Num_Acc", how="left")

    # Merge with characteristics data
    df = df.merge(caract_df, on="Num_Acc", how="left")

    print(f"Full merged dataset shape before filtering: {df.shape}")

    # Remove rows with invalid 'grav' values (-1)
    print(f"Number of rows with grav=-1: {(df['grav'] == -1).sum()}")
    df = df[df['grav'].isin([1, 2, 3, 4])]
    print(f"Dataset shape after filtering out invalid grav values: {df.shape}")

    # Creating the 'securite' column: 1 if any of the 'secu1', 'secu2',
    # or 'secu3' values are greater than 0, otherwise 0
    df["securite"] = ((df["secu1"] > 0) | (df["secu2"] > 0)
                      | (df["secu3"] > 0)).astype(int)

    # Creating the 'age' column by subtracting birth year from current year
    current_year = 2023
    df['age'] = current_year - df['an_nais']

    # Dropping unnecessary columns if they exist in the dataframe
    cols_to_drop = [
        "num_veh", "an", "dep", "v2", "pr", "pr1", "id_usager",
        "id_vehicule", "Num_Acc", "secu2", "secu3", "secu1", "an_nais"
    ]
    df.drop(
        columns=[col for col in cols_to_drop if col in df.columns],
        inplace=True
    )

    # Filling missing values in 'adr' with corresponding values from 'voie'
    df["adr"].fillna(df["voie"], inplace=True)
    df.drop(columns=["voie"], inplace=True)

    # Fill remaining missing values in 'adr' with most frequent value
    mode_adr = df["adr"].mode()[0]
    df["adr"].fillna(mode_adr, inplace=True)

    # Dropping additional unnecessary columns
    df.drop(columns=["occutc", "lartpc"], axis=1, inplace=True)

    # Filling missing values in 'age' with the mean age
    df["age"].fillna(df["age"].mean(), inplace=True)

    # Converting 'nbv' column to string format for further manipulation
    df["nbv"] = df["nbv"].astype(str)

    # Replacing "-1" and "#VALEURMULTI" with NaN values in 'nbv'
    df["nbv"] = df["nbv"].replace({
        "-1": np.nan,
        "#VALEURMULTI": np.nan
    })

    # Converting non-numeric values in 'nbv' to NaN
    df["nbv"] = pd.to_numeric(df["nbv"], errors='coerce')
    median_value = df["nbv"].median()
    # Filling NaN values in 'nbv' with the computed median
    df["nbv"].fillna(median_value, inplace=True)
    df["nbv"] = df["nbv"].astype(int)
    df["actp"] = df["actp"].astype(str)

    # Replacing specific values "-1" and "B" with NaN in 'actp'
    df["actp"] = df["actp"].replace({"-1": np.nan, "B": np.nan})
    # Converting 'actp' to numeric values, ignoring errors
    df["actp"] = pd.to_numeric(df["actp"], errors='coerce')
    median_value = df["actp"].median()
    # Filling NaN values in 'actp' with the computed median
    df["actp"].fillna(median_value, inplace=True)
    df["actp"] = df["actp"].astype(int)

    # Dropping redundant vehicle number columns if they exist
    df.drop(columns=["num_veh_x", "num_veh_y"], inplace=True)

    # Fix 'larrout': replace commas with dots and convert to float
    df["larrout"] = df["larrout"].str.replace(",", ".").astype(float)
    # Fill missing values in 'larrout' with its median
    df["larrout"].fillna(df["larrout"].median(), inplace=True)

    # Extract hour from 'hrmn' and convert to integer
    df["heure"] = df["hrmn"].str.split(":").str[0].astype(int)
    # Drop the original 'hrmn' column
    df.drop(columns=["hrmn"], inplace=True)

    # Fix GPS coordinates: replace commas with dots and convert to float
    df["lat"] = df["lat"].str.replace(",", ".").astype(float)
    df["long"] = df["long"].str.replace(",", ".").astype(float)

    # First split: 80% private data, 20% public data
    print("Splitting data into train/test sets...")
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
    print("Saving datasets...")
    df_private_train.to_csv(data_dir / "train.csv", index=False)
    df_private_test.to_csv(data_dir / "test.csv", index=False)
    df_public_train.to_csv(public_dir / "train.csv", index=False)
    df_public_test.to_csv(public_dir / "test.csv", index=False)

    print("Data preparation complete. Files saved to data/ directory.")


if __name__ == "__main__":
    print("Starting data download and preparation process...")
    data_files = download_data()
    prepare_data(data_files)
    print("Done!")
    sys.exit(0)
