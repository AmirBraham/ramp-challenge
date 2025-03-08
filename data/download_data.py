#!/usr/bin/env python3

import os
import urllib.request
import ssl
import sys
import pandas as pd


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
    
    # Create data directory if it doesn't exist
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Download all files
    success = True
    downloaded_files = []
    
    for dataset_type, info in datasets.items():
        output_file = os.path.join(data_dir, info['filename'])
        print(f"\nDownloading {dataset_type} data...")
        print(f"URL: {info['url']}")
        
        if download_file(info['url'], output_file, context):
            downloaded_files.append(output_file)
        else:
            success = False


if __name__ == "__main__":
    sys.exit(download_data()) 