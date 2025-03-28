from Request_data_noAPI import download_and_process_data, write_scaled_data
import os

def test_abilities_download():
    """Test downloading and processing Abilities data"""
    # Download and process Abilities data
    scaled_data = download_and_process_data(version="29_2", category="Abilities")
    
    if scaled_data:
        # Set up output file path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_DIR = os.path.join(BASE_DIR, 'test', 'example_data')
        output_file = os.path.join(DATA_DIR, 'scaledAbilities.txt')
        
        # Write the scaled data to file
        write_success = write_scaled_data(scaled_data, output_file)
        
        if write_success:
            print("\nSuccessfully wrote scaled data to:", output_file)
        
        print("\nAbilities Data Examples:")
        print("------------------------")
        for i, data in enumerate(scaled_data[:5]):
            print(f"Row {i+1}:")
            print(f"  Original Value: {data['original']}")
            print(f"  Scaled Value: {data['scaled']:.2f}")
            print(f"  Scale ID: {data['scale_id']}")
            print(f"  O*NET-SOC Code: {data['row_data'][0]}")
            print(f"  Element ID: {data['row_data'][1]}")
            print(f"  Element Name: {data['row_data'][2]}")
            print("------------------------")
        
        print(f"\nTotal records processed: {len(scaled_data)}")
    else:
        print("Failed to download or process Abilities data")

if __name__ == "__main__":
    test_abilities_download()
