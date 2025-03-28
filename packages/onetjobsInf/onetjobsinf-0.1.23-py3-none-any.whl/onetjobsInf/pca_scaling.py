import requests
from io import StringIO

class ScaleConverter:
    def __init__(self):
        # URL for the scales reference file
        self.url = "https://www.onetcenter.org/dl_files/database/db_29_2_text/Scales%20Reference.txt"
        self.scales_data = {}
        self._load_scales()
    
    def _load_scales(self):
        """Download and parse the scales reference file"""
        try:
            print("Downloading scales reference file...")
            response = requests.get(self.url)
            response.raise_for_status()
            
            print("Parsing file contents...")
            lines = response.text.strip().split('\n')
            
            # Get header line and split on tabs
            headers = lines[0].strip().split('\t')
            print("Found columns:", headers)
            
            # Store scale information in dictionary
            count = 0
            for line in lines[1:]:  # Skip header row
                values = line.strip().split('\t')
                scale_id = values[0]  # Scale ID is first column
                self.scales_data[scale_id] = {
                    'minimum': float(values[2]),  # Minimum is third column
                    'maximum': float(values[3]),  # Maximum is fourth column  
                    'name': values[1],  # Scale Name is second column
                }
                count += 1
            print(f"Successfully loaded {count} scales")
                
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def scale_value(self, scale_id, x):
        """
        Scale a value using the formula (x-Minimum)*100/(Maximum-Minimum)
        This formula is from https://www.onetonline.org/help/online/scales
        
        Args:
            scale_id (str): The scale ID (e.g., 'IM', 'LV')
            x (float): The value to scale
            
        Returns:
            float: The scaled value between 0 and 100
        """
        if scale_id not in self.scales_data:
            raise ValueError(f"Unknown Scale ID: {scale_id}")
            
        scale = self.scales_data[scale_id]
        minimum = scale['minimum']
        maximum = scale['maximum']
        
        # Apply the scaling formula
        scaled_value = (x - minimum) * 100 / (maximum - minimum)
        return scaled_value
    
    def get_scale_info(self, scale_id):
        """Get information about a particular scale"""
        if scale_id not in self.scales_data:
            raise ValueError(f"Unknown Scale ID: {scale_id}")
        return self.scales_data[scale_id]

# Example usage
if __name__ == "__main__":
    print("Starting Scale Converter...")
    try:
        converter = ScaleConverter()
        
        # Example: Scale a value for the IM (Importance) scale
        value = 3.5
        scale_id = "IM"
        print(f"\nScaling value {value} using scale ID '{scale_id}'")
        
        scaled = converter.scale_value(scale_id, value)
        scale_info = converter.get_scale_info(scale_id)
        
        print(f"\nScaling example for {scale_info['name']}:")
        print(f"Original value: {value}")
        print(f"Scaled value: {scaled:.2f}")
        print(f"Scale range: {scale_info['minimum']} to {scale_info['maximum']}")

        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise  # Re-raise the exception to see the full traceback
