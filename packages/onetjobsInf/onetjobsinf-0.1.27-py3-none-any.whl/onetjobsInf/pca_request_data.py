import requests
from onetjobsInf.pca_scaling import ScaleConverter
import os

def generate_onet_url(version="29_2", category="Skills"):
    """Generate O*NET download URL for given version and category"""
    base_url = "https://www.onetcenter.org/dl_files/database/db_{}_text/{}.txt"
    return base_url.format(version, category)

def download_and_process_data(version="29_2", category="Skills"):
    """Download and process data for any given version and category"""
    # Generate URL and create paths
    url = generate_onet_url(version, category)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'test', 'example_data')
    local_filename = os.path.join(DATA_DIR, f'{category}.txt')
    
    # Create directory if needed
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Download and process
    content = download_file(url, local_filename)
    if content:
        scaled_data = process_and_scale_data(content)
        if scaled_data:
            output_file = os.path.join(DATA_DIR, f'scaled{category}.txt')
            write_scaled_data(scaled_data, output_file)
            return scaled_data
    return None

# Update the URL to use the new function
url = generate_onet_url()

def download_file(url, local_filename):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    content = None
    
    # Check if the request was successful
    if response.status_code == 200:
        content = response.text
        # Open the local file in write mode
        with open(local_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"File downloaded successfully: {local_filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    
    return content

def process_and_scale_data(content):
    """Process the downloaded data and scale values using ScaleConverter"""
    if not content:
        return
        
    converter = ScaleConverter()
    lines = content.strip().split('\n')
    headers = lines[0].split('\t')
    
    # Find required column indices
    try:
        scale_id_idx = headers.index('Scale ID')
        data_value_idx = headers.index('Data Value')
    except ValueError as e:
        print(f"Error: Required column not found - {e}")
        return
        
    # Process each line
    scaled_data = []
    for line in lines[1:]:  # Skip header
        values = line.split('\t')
        if len(values) > max(scale_id_idx, data_value_idx):
            try:
                scale_id = values[scale_id_idx]
                data_value = float(values[data_value_idx])
                scaled_value = converter.scale_value(scale_id, data_value)
                
                # Store original and scaled values
                scaled_data.append({
                    'original': data_value,
                    'scaled': scaled_value,
                    'scale_id': scale_id,
                    'row_data': values
                })
                
            except (ValueError, KeyError) as e:
                print(f"Warning: Could not process line - {e}")
                continue
    
    return scaled_data

def write_scaled_data(scaled_data, output_filename):
    """Write scaled data to a tab-delimited file"""
    if not scaled_data:
        return False
        
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write("O*NET-SOC Code\tElement ID\tElement Name\tOriginal Value\tScaled Value\tScale ID\n")
            
            # Write data rows
            for data in scaled_data:
                row = data['row_data']
                f.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{data['original']}\t{data['scaled']:.2f}\t{data['scale_id']}\n")
        
        print(f"Scaled data written to: {output_filename}")
        return True
    except Exception as e:
        print(f"Error writing scaled data: {e}")
        return False

if __name__ == "__main__":
    # Example using the new flexible function
    scaled_data = download_and_process_data("29_2", "Skills")
    if scaled_data:
        print("\nScaled Data Examples:")
        for i, data in enumerate(scaled_data[:5]):
            print(f"Row {i+1}: Original={data['original']}, "
                  f"Scaled={data['scaled']:.2f} "
                  f"(Scale ID: {data['scale_id']})")