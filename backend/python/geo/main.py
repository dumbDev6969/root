import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class PSGCDataDownloader:
    def __init__(self, base_url="https://psgc.gitlab.io/api"):
        self.base_url = base_url
        self.output_dir = "psgc_data"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_data(self, endpoint):
        """
        Fetch data from a specific PSGC API endpoint
        """
        try:
            full_url = f"{self.base_url}/{endpoint}"
            response = requests.get(full_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def save_json(self, filename, data):
        """
        Save data to a JSON file
        """
        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved {filename}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")

    def download_endpoints(self, endpoints):
        """
        Download multiple endpoints concurrently
        """
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Create a list to store future tasks
            future_to_endpoint = {
                executor.submit(self.fetch_data, endpoint): endpoint 
                for endpoint in endpoints
            }

            # Process results as they complete
            for future in as_completed(future_to_endpoint):
                endpoint = future_to_endpoint[future]
                try:
                    data = future.result()
                    if data:
                        # Generate filename based on endpoint
                        filename = f"{endpoint.replace('/', '_')}.json"
                        self.save_json(filename, data)
                except Exception as e:
                    print(f"Error processing {endpoint}: {e}")

    def process_data_with_metadata(self, endpoints):
        """
        Advanced data processing with additional metadata
        """
        processed_data = {}
        
        for endpoint in endpoints:
            data = self.fetch_data(endpoint)
            if data:
                processed_data[endpoint] = {
                    "total_records": len(data),
                    "sample_records": data[:5],  # First 5 records as sample
                    "full_data": data
                }
                
                # Save full and metadata files
                self.save_json(f"{endpoint.replace('/', '_')}_full.json", data)
                self.save_json(f"{endpoint.replace('/', '_')}_metadata.json", processed_data[endpoint])

        return processed_data

    def generate_summary_report(self, processed_data):
        """
        Generate a comprehensive summary report
        """
        summary = {
            "total_endpoints": len(processed_data),
            "endpoint_details": {}
        }

        for endpoint, data in processed_data.items():
            summary["endpoint_details"][endpoint] = {
                "total_records": data["total_records"],
                "first_record_sample": data["sample_records"]
            }

        self.save_json("psgc_summary_report.json", summary)

def main():
    # Initialize downloader
    downloader = PSGCDataDownloader()

    # Endpoints to download
    endpoints = [
        "barangays",
        "provinces", 
        "municipalities"
    ]

    # Download endpoints
    downloader.download_endpoints(endpoints)

    # Process with metadata
    processed_data = downloader.process_data_with_metadata(endpoints)

    # Generate summary report
    downloader.generate_summary_report(processed_data)

    print("PSGC Data download and processing complete!")

if __name__ == "__main__":
    main()