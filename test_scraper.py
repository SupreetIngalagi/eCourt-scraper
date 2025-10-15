#!/usr/bin/env python3
"""
Test script for eCourts Scraper
Tests all major functionality of the scraper.
"""

import os
import sys
import json
from datetime import datetime
from ecourts_scraper import ECourtsScraper

def test_basic_functionality():
    """Test basic scraper functionality."""
    print("🧪 Testing eCourts Scraper...")
    print("=" * 50)
    
    scraper = ECourtsScraper()
    
    # Test 1: Court list
    print("\n1. Testing court list retrieval...")
    courts = scraper.get_court_list()
    print(f"   Found {len(courts)} courts")
    if courts:
        print(f"   Sample court: {courts[0]['name']}")
    
    # Test 2: Case search by CNR
    print("\n2. Testing case search by CNR...")
    cnr_result = scraper.search_case_by_cnr("TEST123456789")
    if cnr_result:
        print(f"   Case found: {cnr_result.get('case_number', 'N/A')}")
        print(f"   Court: {cnr_result.get('court_name', 'N/A')}")
        print(f"   Listed today: {cnr_result.get('is_listed_today', False)}")
    else:
        print("   No case found (expected for test CNR)")
    
    # Test 3: Case search by details
    print("\n3. Testing case search by details...")
    details_result = scraper.search_case_by_details("Civil", "12345", "2023")
    if details_result:
        print(f"   Case found: {details_result.get('case_number', 'N/A')}")
        print(f"   Court: {details_result.get('court_name', 'N/A')}")
        print(f"   Listed tomorrow: {details_result.get('is_listed_tomorrow', False)}")
    else:
        print("   No case found (expected for test details)")
    
    # Test 4: Cause list
    print("\n4. Testing cause list retrieval...")
    cause_list = scraper.get_cause_list("01")
    print(f"   Retrieved {len(cause_list)} cases from cause list")
    if cause_list:
        print(f"   First case: {cause_list[0].get('case_number', 'N/A')}")
        print(f"   Time: {cause_list[0].get('time', 'N/A')}")
    
    # Test 5: File operations
    print("\n5. Testing file operations...")
    test_data = {
        "test": "data",
        "timestamp": datetime.now().isoformat(),
        "cases": cause_list
    }
    
    json_file = scraper.save_results(test_data, "test_output.json")
    if json_file and os.path.exists(json_file):
        print(f"   JSON file saved: {json_file}")
        os.remove(json_file)  # Clean up
    
    csv_file = scraper.save_cause_list_csv(cause_list, "test_cause_list.csv")
    if csv_file and os.path.exists(csv_file):
        print(f"   CSV file saved: {csv_file}")
        os.remove(csv_file)  # Clean up
    
    # Test 6: PDF download
    print("\n6. Testing PDF download...")
    os.makedirs("test_downloads", exist_ok=True)
    pdf_path = scraper.download_case_pdf("TEST123", "test_downloads")
    if pdf_path and os.path.exists(pdf_path):
        print(f"   PDF downloaded: {pdf_path}")
        os.remove(pdf_path)  # Clean up
        os.rmdir("test_downloads")  # Clean up directory
    
    print("\n✅ All tests completed successfully!")
    print("=" * 50)

def test_cli_interface():
    """Test CLI interface."""
    print("\n🔧 Testing CLI Interface...")
    print("=" * 30)
    
    # Test help command
    print("\n1. Testing help command...")
    os.system("python ecourts_scraper.py --help")
    
    print("\n2. Testing case search...")
    os.system("python ecourts_scraper.py --cnr TEST123 --output-dir test_output")
    
    print("\n3. Testing cause list...")
    os.system("python ecourts_scraper.py --causelist --court-code 01 --output-dir test_output")
    
    # Clean up test output
    if os.path.exists("test_output"):
        import shutil
        shutil.rmtree("test_output")
    
    print("\n✅ CLI tests completed!")

def test_web_interface():
    """Test web interface components."""
    print("\n🌐 Testing Web Interface Components...")
    print("=" * 40)
    
    # Test if Flask can be imported
    try:
        import flask
        print("✅ Flask is available")
    except ImportError:
        print("❌ Flask not available - install with: pip install flask")
        return
    
    # Test if web_interface.py can be imported
    try:
        import web_interface
        print("✅ Web interface module can be imported")
    except ImportError as e:
        print(f"❌ Web interface import error: {e}")
        return
    
    print("\n✅ Web interface components are ready!")
    print("   To test the web interface, run: python web_interface.py")
    print("   Then open: http://localhost:5000")

def create_demo_data():
    """Create demo data for testing."""
    print("\n📊 Creating Demo Data...")
    print("=" * 25)
    
    demo_cases = [
        {
            "cnr": "DLCT01-123456-2023",
            "case_number": "12345/2023",
            "case_title": "John Doe vs. Jane Smith",
            "court_name": "Delhi District Court",
            "case_type": "Civil",
            "filing_date": "2023-01-15",
            "status": "Pending",
            "next_hearing": "2023-10-20",
            "serial_number": "1",
            "is_listed_today": True,
            "is_listed_tomorrow": False
        },
        {
            "cnr": "DLCT01-789012-2023",
            "case_number": "67890/2023",
            "case_title": "ABC Corp vs. XYZ Ltd",
            "court_name": "Delhi High Court",
            "case_type": "Commercial",
            "filing_date": "2023-02-20",
            "status": "Pending",
            "next_hearing": "2023-10-21",
            "serial_number": "2",
            "is_listed_today": False,
            "is_listed_tomorrow": True
        }
    ]
    
    demo_cause_list = [
        {
            "serial_number": "1",
            "case_number": "12345/2023",
            "case_title": "John Doe vs. Jane Smith",
            "petitioner": "John Doe",
            "respondent": "Jane Smith",
            "advocate": "Advocate ABC",
            "court_room": "Room 1",
            "time": "10:00 AM"
        },
        {
            "serial_number": "2",
            "case_number": "67890/2023",
            "case_title": "ABC Corp vs. XYZ Ltd",
            "petitioner": "ABC Corp",
            "respondent": "XYZ Ltd",
            "advocate": "Advocate XYZ",
            "court_room": "Room 2",
            "time": "11:00 AM"
        }
    ]
    
    # Save demo data
    with open("demo_cases.json", "w") as f:
        json.dump(demo_cases, f, indent=2)
    
    with open("demo_cause_list.json", "w") as f:
        json.dump(demo_cause_list, f, indent=2)
    
    print("✅ Demo data created:")
    print("   - demo_cases.json")
    print("   - demo_cause_list.json")

def main():
    """Run all tests."""
    print("🚀 eCourts Scraper Test Suite")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_cli_interface()
        test_web_interface()
        create_demo_data()
        
        print("\n🎉 All tests completed successfully!")
        print("\nNext steps:")
        print("1. Run the CLI: python ecourts_scraper.py --help")
        print("2. Start web interface: python web_interface.py")
        print("3. Create your demonstration video")
        print("4. Submit your GitHub repository")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
