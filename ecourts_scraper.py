#!/usr/bin/env python3
"""
eCourts Scraper - Intern Task
A Python script to fetch court listings from eCourts India portal.
"""

import requests
import json
import csv
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import click
import logging
from bs4 import BeautifulSoup
import time
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecourts_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ECourtsScraper:
    """Main class for scraping eCourts data."""
    
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Demo dataset for offline/demo purposes
        self.demo_cases = {
            "DLCT01-123456-2023": {
                "cnr": "DLCT01-123456-2023",
                "case_number": "12345/2023",
                "case_title": "John Doe vs. Jane Smith",
                "court_name": "Delhi High Court",
                "case_type": "Civil",
                "filing_date": "2023-01-15",
                "status": "Pending",
                "next_hearing": "2025-10-20",
                "serial_number": "1",
                "is_listed_today": True,
                "is_listed_tomorrow": False
            },
            "MHMC02-654321-2022": {
                "cnr": "MHMC02-654321-2022",
                "case_number": "65432/2022",
                "case_title": "ABC Pvt Ltd vs. XYZ Traders",
                "court_name": "Mumbai City Civil Court",
                "case_type": "Commercial",
                "filing_date": "2022-06-10",
                "status": "Pending",
                "next_hearing": "2025-10-21",
                "serial_number": "7",
                "is_listed_today": False,
                "is_listed_tomorrow": True
            },
            "KLER03-111222-2021": {
                "cnr": "KLER03-111222-2021",
                "case_number": "11122/2021",
                "case_title": "State vs. Raman Nair",
                "court_name": "Ernakulam District Court",
                "case_type": "Criminal",
                "filing_date": "2021-09-05",
                "status": "Listed",
                "next_hearing": "2025-10-15",
                "serial_number": "15",
                "is_listed_today": True,
                "is_listed_tomorrow": False
            },
            "TNCH04-777888-2020": {
                "cnr": "TNCH04-777888-2020",
                "case_number": "77788/2020",
                "case_title": "Mohan vs. Housing Board",
                "court_name": "Chennai City Civil Court",
                "case_type": "Civil",
                "filing_date": "2020-11-20",
                "status": "Adjourned",
                "next_hearing": "2025-10-22",
                "serial_number": "23",
                "is_listed_today": False,
                "is_listed_tomorrow": True
            },
            "RJJP05-333444-2019": {
                "cnr": "RJJP05-333444-2019",
                "case_number": "33344/2019",
                "case_title": "Pooja Sharma vs. RTO Jaipur",
                "court_name": "Jaipur District Court",
                "case_type": "Motor Accident Claims",
                "filing_date": "2019-03-18",
                "status": "For Hearing",
                "next_hearing": "2025-10-16",
                "serial_number": "3",
                "is_listed_today": True,
                "is_listed_tomorrow": False
            }
        }
        
    def get_court_list(self) -> List[Dict]:
        """Get list of available courts."""
        try:
            # This would typically involve scraping the court selection page
            # For now, returning a sample structure
            courts = [
                {"code": "01", "name": "Supreme Court of India", "type": "Supreme Court"},
                {"code": "02", "name": "Delhi High Court", "type": "High Court"},
                {"code": "03", "name": "Mumbai High Court", "type": "High Court"},
                # Add more courts as needed
            ]
            return courts
        except Exception as e:
            logger.error(f"Error fetching court list: {e}")
            return []
    
    def search_case_by_cnr(self, cnr: str) -> Dict:
        """Search for a case using CNR (Case Number Record)."""
        try:
            logger.info(f"Searching for case with CNR: {cnr}")
            
            # Return demo case if available
            if cnr in self.demo_cases:
                return self.demo_cases[cnr]
            
            # Fallback demo when unknown CNR is provided
            return {}
            
        except Exception as e:
            logger.error(f"Error searching case by CNR: {e}")
            return {}
    
    def search_case_by_details(self, case_type: str, case_number: str, year: str) -> Dict:
        """Search for a case using case type, number, and year."""
        try:
            logger.info(f"Searching for case: {case_type}/{case_number}/{year}")
            
            # Placeholder implementation
            result = {
                "case_type": case_type,
                "case_number": case_number,
                "year": year,
                "case_title": f"Sample {case_type} Case",
                "court_name": "District Court",
                "filing_date": "2023-01-15",
                "status": "Pending",
                "next_hearing": "2023-10-21",
                "serial_number": "2",
                "is_listed_today": False,
                "is_listed_tomorrow": True
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching case by details: {e}")
            return {}
    
    def get_cause_list(self, court_code: str, date: str = None) -> List[Dict]:
        """Get cause list for a specific court and date."""
        try:
            if not date:
                date = datetime.now().strftime("%d/%m/%Y")
            
            logger.info(f"Fetching cause list for court {court_code} on {date}")
            
            # Placeholder implementation
            cause_list = [
                {
                    "serial_number": "1",
                    "case_number": "12345/2023",
                    "case_title": "Sample Case 1",
                    "petitioner": "John Doe",
                    "respondent": "Jane Smith",
                    "advocate": "Advocate ABC",
                    "court_room": "Room 1",
                    "time": "10:00 AM"
                },
                {
                    "serial_number": "2",
                    "case_number": "67890/2023",
                    "case_title": "Sample Case 2",
                    "petitioner": "Alice Johnson",
                    "respondent": "Bob Wilson",
                    "advocate": "Advocate XYZ",
                    "court_room": "Room 2",
                    "time": "11:00 AM"
                },
                {
                    "serial_number": "3",
                    "case_number": "22222/2022",
                    "case_title": "Ravi Kumar vs. State",
                    "petitioner": "Ravi Kumar",
                    "respondent": "State",
                    "advocate": "Adv. Mehta",
                    "court_room": "Room 3",
                    "time": "11:30 AM"
                },
                {
                    "serial_number": "4",
                    "case_number": "33333/2021",
                    "case_title": "Sita Devi vs. Nagar Nigam",
                    "petitioner": "Sita Devi",
                    "respondent": "Nagar Nigam",
                    "advocate": "Adv. Rao",
                    "court_room": "Room 4",
                    "time": "12:00 PM"
                },
                {
                    "serial_number": "5",
                    "case_number": "44444/2020",
                    "case_title": "Om Prakash vs. Insurance Co.",
                    "petitioner": "Om Prakash",
                    "respondent": "National Insurance",
                    "advocate": "Adv. Khan",
                    "court_room": "Room 5",
                    "time": "12:30 PM"
                }
            ]
            
            return cause_list
            
        except Exception as e:
            logger.error(f"Error fetching cause list: {e}")
            return []
    
    def download_case_pdf(self, case_id: str, output_dir: str = "downloads") -> str:
        """Download case PDF if available."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Placeholder for PDF download
            # In reality, you would need to:
            # 1. Find the PDF link in the case details
            # 2. Download the PDF
            # 3. Save it to the specified directory
            
            # Sanitize case_id for safe filenames (replace slashes and illegal chars)
            safe_case_id = re.sub(r"[^A-Za-z0-9_-]+", "_", str(case_id))
            pdf_path = os.path.join(output_dir, f"case_{safe_case_id}.pdf")
            
            # For demonstration, creating a dummy file
            with open(pdf_path, 'w') as f:
                f.write("This is a placeholder PDF content")
            
            logger.info(f"PDF downloaded to: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error downloading PDF: {e}")
            return ""
    
    def save_results(self, data: Dict, filename: str = None) -> str:
        """Save results to JSON file."""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ecourts_results_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return ""
    
    def save_cause_list_csv(self, cause_list: List[Dict], filename: str = None) -> str:
        """Save cause list to CSV file."""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"cause_list_{timestamp}.csv"
            
            if not cause_list:
                logger.warning("No cause list data to save")
                return ""
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=cause_list[0].keys())
                writer.writeheader()
                writer.writerows(cause_list)
            
            logger.info(f"Cause list saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving cause list: {e}")
            return ""

@click.command()
@click.option('--cnr', help='Case Number Record (CNR) to search')
@click.option('--case-type', help='Case type')
@click.option('--case-number', help='Case number')
@click.option('--year', help='Case year')
@click.option('--today', is_flag=True, help='Check cases listed today')
@click.option('--tomorrow', is_flag=True, help='Check cases listed tomorrow')
@click.option('--causelist', is_flag=True, help='Download cause list')
@click.option('--court-code', default='01', help='Court code for cause list')
@click.option('--output-dir', default='output', help='Output directory for files')
@click.option('--download-pdf', is_flag=True, help='Download case PDF if available')
def main(cnr, case_type, case_number, year, today, tomorrow, causelist, court_code, output_dir, download_pdf):
    """eCourts Scraper - Main CLI interface."""
    
    scraper = ECourtsScraper()
    results = {}
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Search by CNR
        if cnr:
            logger.info("Searching by CNR...")
            case_result = scraper.search_case_by_cnr(cnr)
            if case_result:
                results['case_search'] = case_result
                print(f"\nCase found:")
                print(f"CNR: {case_result.get('cnr', 'N/A')}")
                print(f"Case Number: {case_result.get('case_number', 'N/A')}")
                print(f"Court: {case_result.get('court_name', 'N/A')}")
                print(f"Serial Number: {case_result.get('serial_number', 'N/A')}")
                print(f"Listed Today: {case_result.get('is_listed_today', False)}")
                print(f"Listed Tomorrow: {case_result.get('is_listed_tomorrow', False)}")
                
                if download_pdf and case_result.get('case_number'):
                    pdf_path = scraper.download_case_pdf(case_result['case_number'], output_dir)
                    if pdf_path:
                        results['pdf_downloaded'] = pdf_path
        
        # Search by case details
        elif case_type and case_number and year:
            logger.info("Searching by case details...")
            case_result = scraper.search_case_by_details(case_type, case_number, year)
            if case_result:
                results['case_search'] = case_result
                print(f"\nCase found:")
                print(f"Case: {case_result.get('case_type', 'N/A')}/{case_result.get('case_number', 'N/A')}/{case_result.get('year', 'N/A')}")
                print(f"Court: {case_result.get('court_name', 'N/A')}")
                print(f"Serial Number: {case_result.get('serial_number', 'N/A')}")
                print(f"Listed Today: {case_result.get('is_listed_today', False)}")
                print(f"Listed Tomorrow: {case_result.get('is_listed_tomorrow', False)}")
        
        # Get cause list
        if causelist:
            logger.info("Fetching cause list...")
            cause_list = scraper.get_cause_list(court_code)
            if cause_list:
                results['cause_list'] = cause_list
                print(f"\nCause list fetched with {len(cause_list)} cases:")
                for case in cause_list[:5]:  # Show first 5 cases
                    print(f"Serial: {case.get('serial_number', 'N/A')} | Case: {case.get('case_number', 'N/A')} | Time: {case.get('time', 'N/A')}")
                
                # Save cause list to CSV
                csv_file = scraper.save_cause_list_csv(cause_list, os.path.join(output_dir, "cause_list.csv"))
                if csv_file:
                    results['cause_list_file'] = csv_file
        
        # Save all results
        if results:
            json_file = scraper.save_results(results, os.path.join(output_dir, "results.json"))
            if json_file:
                print(f"\nAll results saved to: {json_file}")
        
        # Show summary
        print(f"\n{'='*50}")
        print("SUMMARY")
        print(f"{'='*50}")
        print(f"Output directory: {output_dir}")
        print(f"Results saved: {len(results)} items")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
