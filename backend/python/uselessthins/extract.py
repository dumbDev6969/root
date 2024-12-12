import requests
from bs4 import BeautifulSoup
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional
import time

class JobScraper:
    """A class to scrape job listings from JobStreet Philippines."""
    
    def __init__(self, max_workers: int = 100, base_url: str = "https://ph.jobstreet.com"):
        """
        Initialize the JobScraper.
        
        Args:
            max_workers: Maximum number of concurrent threads
            base_url: Base URL for JobStreet website
        """
        self.max_workers = max_workers
        self.base_url = base_url
        self.session = requests.Session()
        self.setup_logging()

    def setup_logging(self):
        """Configure logging settings."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def extract_data(self, page_number: int) -> str:
        """
        Extract job listings data from a specific page.
        
        Args:
            page_number: Page number to scrape
            
        Returns:
            JSON string containing page data
        """
        url = f"{self.base_url}/jobs?classification=1223%2C6281%2C6304%3Fpage%3D1000%2C6251%2C6304%2C1204&page={page_number}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tag = soup.find('script', attrs={'data-automation': 'server-state'})
            
            if not script_tag or not script_tag.contents:
                raise ValueError(f"No script tag found on page {page_number}")
                
            script_content = script_tag.contents[0]
            start_index = script_content.find("window.SEEK_REDUX_DATA = ")
            end_index = script_content.find("};", start_index)
            
            if start_index == -1 or end_index == -1:
                raise ValueError(f"Could not find data boundaries on page {page_number}")
                
            data_str = script_content[start_index:end_index+1]
            return data_str.split(" = ")[1]
            
        except Exception as e:
            self.logger.error(f"Error extracting data from page {page_number}: {str(e)}")
            return "{}"

    def extract_job(self, job_id: str) -> Dict:
        """
        Extract detailed information for a specific job.
        
        Args:
            job_id: Job ID to scrape
            
        Returns:
            Dictionary containing job details
        """
        url = f"{self.base_url}/job/{job_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.find_all('script', attrs={'data-rh': 'true', 'type': 'application/ld+json'})
           
            if len(script_tags) > 1 and script_tags[1].contents:
                return json.loads(script_tags[1].contents[0])
            else:
                return {'error': 'Job listing not found or no longer available'}
                
        except Exception as e:
            self.logger.error(f"Error extracting job {job_id}: {str(e)}")
            return {'error': f'Failed to extract job: {str(e)}'}

    def scrape_all_pages(self, start_page: int = 1, end_page: int = 838) -> None:
        """
        Scrape job listings from multiple pages and save to file.
        
        Args:
            start_page: First page to scrape
            end_page: Last page to scrape
        """
        data_list = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.extract_data, i): i for i in range(start_page, end_page + 1)}
            
            for future in as_completed(futures):
                result = future.result()
                if result != "{}":
                    data_list.append(result)
                    
        self.save_to_file(data_list, 'jobs.json')
        self.logger.info(f"Saved {len(data_list)} pages of job listings")

    def process_jobs(self, input_file: str = 'jobs.json', output_file: str = 'jobs_data.json') -> None:
        """
        Process job listings and extract detailed information.
        
        Args:
            input_file: JSON file containing job listings
            output_file: Output file for detailed job data
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading input file: {str(e)}")
            return

        jobs_data = {}
        futures = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for data in data_list:
                try:
                    jobs = json.loads(data)['results']['results']['jobs']
                    for job in jobs:
                        job_id = job["advertiser"]['id']
                        futures[executor.submit(self.extract_job, job_id)] = job_id
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error decoding JSON: {str(e)}")
                    continue

            for future in as_completed(futures):
                job_id = futures[future]
                try:
                    result = future.result()
                    if 'error' not in result:
                        jobs_data[job_id] = result
                except Exception as e:
                    self.logger.error(f"Error processing job {job_id}: {str(e)}")

        self.save_to_file(jobs_data, output_file)
        self.logger.info(f"Saved {len(jobs_data)} detailed job listings")

    def save_to_file(self, data: Dict, filename: str) -> None:
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving to {filename}: {str(e)}")

if __name__ == "__main__":
    # Example usage
    scraper = JobScraper(max_workers=100)
    job=scraper.extract_job("80428095")
    print(job)  
    
  