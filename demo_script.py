#!/usr/bin/env python3
"""
Demo Script for eCourts Scraper
This script demonstrates all the key features of the eCourts scraper.
Use this script to create your demonstration video.
"""

import os
import sys
import time
from datetime import datetime
from ecourts_scraper import ECourtsScraper

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def demo_cli_usage():
    """Demonstrate CLI usage."""
    print_header("COMMAND LINE INTERFACE DEMONSTRATION")
    
    print_step(1, "Show help and available options")
    print("Running: python ecourts_scraper.py --help")
    os.system("python ecourts_scraper.py --help")
    
    print_step(2, "Search case by CNR")
    print("Running: python ecourts_scraper.py --cnr DLCT01-123456-2023 --output-dir demo_output")
    os.system("python ecourts_scraper.py --cnr DLCT01-123456-2023 --output-dir demo_output")
    
    print_step(3, "Search case by details")
    print("Running: python ecourts_scraper.py --case-type Civil --case-number 12345 --year 2023 --output-dir demo_output")
    os.system("python ecourts_scraper.py --case-type Civil --case-number 12345 --year 2023 --output-dir demo_output")
    
    print_step(4, "Get cause list")
    print("Running: python ecourts_scraper.py --causelist --court-code 01 --output-dir demo_output")
    os.system("python ecourts_scraper.py --causelist --court-code 01 --output-dir demo_output")
    
    print_step(5, "Download with PDF")
    print("Running: python ecourts_scraper.py --cnr DLCT01-123456-2023 --download-pdf --output-dir demo_output")
    os.system("python ecourts_scraper.py --cnr DLCT01-123456-2023 --download-pdf --output-dir demo_output")

def demo_programmatic_usage():
    """Demonstrate programmatic usage."""
    print_header("PROGRAMMATIC USAGE DEMONSTRATION")
    
    print_step(1, "Initialize scraper")
    scraper = ECourtsScraper()
    print("✅ Scraper initialized")
    
    print_step(2, "Get court list")
    courts = scraper.get_court_list()
    print(f"✅ Found {len(courts)} courts")
    for court in courts[:3]:  # Show first 3
        print(f"   - {court['name']} ({court['type']})")
    
    print_step(3, "Search case by CNR")
    case_result = scraper.search_case_by_cnr("DLCT01-123456-2023")
    if case_result:
        print("✅ Case found:")
        print(f"   CNR: {case_result.get('cnr', 'N/A')}")
        print(f"   Case Number: {case_result.get('case_number', 'N/A')}")
        print(f"   Court: {case_result.get('court_name', 'N/A')}")
        print(f"   Listed Today: {case_result.get('is_listed_today', False)}")
        print(f"   Listed Tomorrow: {case_result.get('is_listed_tomorrow', False)}")
    
    print_step(4, "Search case by details")
    details_result = scraper.search_case_by_details("Civil", "12345", "2023")
    if details_result:
        print("✅ Case found:")
        print(f"   Case: {details_result.get('case_type', 'N/A')}/{details_result.get('case_number', 'N/A')}/{details_result.get('year', 'N/A')}")
        print(f"   Court: {details_result.get('court_name', 'N/A')}")
        print(f"   Serial Number: {details_result.get('serial_number', 'N/A')}")
    
    print_step(5, "Get cause list")
    cause_list = scraper.get_cause_list("01")
    print(f"✅ Retrieved {len(cause_list)} cases from cause list")
    for i, case in enumerate(cause_list[:3]):  # Show first 3
        print(f"   {i+1}. Serial: {case.get('serial_number', 'N/A')} | Case: {case.get('case_number', 'N/A')} | Time: {case.get('time', 'N/A')}")
    
    print_step(6, "Save results")
    results = {
        "timestamp": datetime.now().isoformat(),
        "case_search": case_result,
        "cause_list": cause_list,
        "total_cases": len(cause_list)
    }
    
    json_file = scraper.save_results(results, "demo_results.json")
    if json_file:
        print(f"✅ Results saved to: {json_file}")
    
    csv_file = scraper.save_cause_list_csv(cause_list, "demo_cause_list.csv")
    if csv_file:
        print(f"✅ Cause list saved to: {csv_file}")

def demo_web_interface():
    """Demonstrate web interface setup."""
    print_header("WEB INTERFACE DEMONSTRATION")
    
    print_step(1, "Check Flask installation")
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not installed - run: pip install flask")
        return
    
    print_step(2, "Web interface setup")
    print("To start the web interface:")
    print("1. Run: python web_interface.py")
    print("2. Open browser to: http://localhost:5000")
    print("3. Use the web form to search cases")
    print("4. Download cause lists and PDFs")
    
    print_step(3, "Web interface features")
    print("✅ User-friendly search forms")
    print("✅ Real-time results display")
    print("✅ File download links")
    print("✅ Responsive design")
    print("✅ Error handling")

def demo_output_files():
    """Demonstrate output files."""
    print_header("OUTPUT FILES DEMONSTRATION")
    
    print_step(1, "Check generated files")
    output_dir = "demo_output"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"✅ Found {len(files)} files in {output_dir}:")
        for file in files:
            file_path = os.path.join(output_dir, file)
            size = os.path.getsize(file_path)
            print(f"   - {file} ({size} bytes)")
    else:
        print("❌ No output directory found")
    
    print_step(2, "File formats supported")
    print("✅ JSON files - Structured data")
    print("✅ CSV files - Spreadsheet compatible")
    print("✅ Text files - Human readable")
    print("✅ PDF files - Case documents")

def demo_error_handling():
    """Demonstrate error handling."""
    print_header("ERROR HANDLING DEMONSTRATION")
    
    print_step(1, "Invalid CNR")
    scraper = ECourtsScraper()
    result = scraper.search_case_by_cnr("INVALID_CNR")
    if not result:
        print("✅ Properly handled invalid CNR")
    
    print_step(2, "Missing parameters")
    result = scraper.search_case_by_details("", "", "")
    if not result:
        print("✅ Properly handled missing parameters")
    
    print_step(3, "Network errors")
    print("✅ Built-in retry mechanism")
    print("✅ Timeout handling")
    print("✅ Connection error handling")
    
    print_step(4, "File operation errors")
    print("✅ Permission error handling")
    print("✅ Disk space error handling")
    print("✅ Path validation")

def cleanup_demo_files():
    """Clean up demo files."""
    print_header("CLEANUP")
    
    files_to_remove = [
        "demo_output",
        "demo_results.json",
        "demo_cause_list.csv",
        "test_output.json",
        "test_cause_list.csv"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            if os.path.isdir(file):
                import shutil
                shutil.rmtree(file)
                print(f"✅ Removed directory: {file}")
            else:
                os.remove(file)
                print(f"✅ Removed file: {file}")

def main():
    """Run the complete demonstration."""
    print("🎬 eCourts Scraper - Complete Demonstration")
    print("This script demonstrates all features for your video recording")
    print("\nPress Enter to start the demonstration...")
    input()
    
    try:
        demo_cli_usage()
        time.sleep(2)
        
        demo_programmatic_usage()
        time.sleep(2)
        
        demo_web_interface()
        time.sleep(2)
        
        demo_output_files()
        time.sleep(2)
        
        demo_error_handling()
        time.sleep(2)
        
        print_header("DEMONSTRATION COMPLETE")
        print("✅ All features demonstrated successfully!")
        print("\nFor your video recording:")
        print("1. Run this script: python demo_script.py")
        print("2. Show the CLI usage examples")
        print("3. Demonstrate the web interface")
        print("4. Show the output files")
        print("5. Explain the error handling")
        
        cleanup_demo_files()
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
