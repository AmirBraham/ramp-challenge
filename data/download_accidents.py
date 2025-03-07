#!/usr/bin/env python3

import os
import urllib.request
import ssl
import sys


def download_data():
    """
    Download the CSV file from the data.gouv.fr website
    """
    # URL of the CSV file
    url = ("https://www.data.gouv.fr/fr/datasets/r/"
           "6af37c98-0933-4ae4-8380-5f63212fb52a")
    
    # Define the output file path
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               "accidents_data.csv")
    
    print(f"Downloading data from {url}...")
    
    try:
        # Create an SSL context that ignores certificate verification
        # Note: This is not recommended for production use but can help bypass 
        # SSL issues
        context = ssl._create_unverified_context()
        
        # Use urllib.request.urlopen with the SSL context
        with urllib.request.urlopen(url, context=context) as response:
            data = response.read()
            
            # Write the data to a file
            with open(output_file, 'wb') as file:
                file.write(data)
                
        print(f"Data successfully downloaded to {output_file}")
    except Exception as e:
        print(f"Error downloading the file: {e}", file=sys.stderr)
        print("\nAlternative download methods:")
        print("1. Try downloading manually and placing in the data directory")
        print("2. Use curl or wget from the command line:")
        print(f"   curl -o data/accidents_data.csv '{url}'")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(download_data()) 