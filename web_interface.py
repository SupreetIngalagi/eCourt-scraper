#!/usr/bin/env python3
"""
Web Interface for eCourts Scraper
A simple Flask web interface for the eCourts scraper.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from ecourts_scraper import ECourtsScraper

app = Flask(__name__)
scraper = ECourtsScraper()

@app.route('/')
def index():
    """Main page with search form."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_case():
    """Search for a case."""
    try:
        data = request.get_json()
        search_type = data.get('search_type')
        
        if search_type == 'cnr':
            cnr = data.get('cnr')
            if not cnr:
                return jsonify({'error': 'CNR is required'}), 400
            
            result = scraper.search_case_by_cnr(cnr)
            
        elif search_type == 'details':
            case_type = data.get('case_type')
            case_number = data.get('case_number')
            year = data.get('year')
            
            if not all([case_type, case_number, year]):
                return jsonify({'error': 'All case details are required'}), 400
            
            result = scraper.search_case_by_details(case_type, case_number, year)
            
        else:
            return jsonify({'error': 'Invalid search type'}), 400
        
        if result:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': 'Case not found'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/causelist', methods=['POST'])
def get_cause_list():
    """Get cause list for a court."""
    try:
        data = request.get_json()
        court_code = data.get('court_code', '01')
        date = data.get('date')
        
        cause_list = scraper.get_cause_list(court_code, date)
        
        if cause_list:
            # Save to file
            filename = scraper.save_cause_list_csv(cause_list)
            return jsonify({
                'success': True, 
                'data': cause_list,
                'filename': filename
            })
        else:
            return jsonify({'success': False, 'message': 'No cause list found'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download a file."""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/courts')
def get_courts():
    """Get list of available courts."""
    try:
        courts = scraper.get_court_list()
        return jsonify({'success': True, 'data': courts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory and HTML file
    os.makedirs('templates', exist_ok=True)
    
    # Create basic HTML template
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>eCourts Scraper</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .error {
            border-left-color: #dc3545;
            background-color: #f8d7da;
        }
        .success {
            border-left-color: #28a745;
            background-color: #d4edda;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>eCourts Case Scraper</h1>
        
        <div class="form-group">
            <label>Search Type:</label>
            <select id="searchType">
                <option value="cnr">Search by CNR</option>
                <option value="details">Search by Case Details</option>
            </select>
        </div>
        
        <div id="cnrForm">
            <div class="form-group">
                <label for="cnr">CNR (Case Number Record):</label>
                <input type="text" id="cnr" placeholder="Enter CNR">
            </div>
        </div>
        
        <div id="detailsForm" style="display: none;">
            <div class="form-group">
                <label for="caseType">Case Type:</label>
                <input type="text" id="caseType" placeholder="e.g., Civil, Criminal">
            </div>
            <div class="form-group">
                <label for="caseNumber">Case Number:</label>
                <input type="text" id="caseNumber" placeholder="Enter case number">
            </div>
            <div class="form-group">
                <label for="year">Year:</label>
                <input type="text" id="year" placeholder="e.g., 2023">
            </div>
        </div>
        
        <button id="btnSearch" type="button">Search Case</button>
        <button id="btnCause" type="button">Get Cause List</button>
        
        <div id="result"></div>
    </div>

    <script>
        // Ensure buttons always wire up, even if attributes are stripped or cached
        document.addEventListener('DOMContentLoaded', function() {
            const btnSearch = document.getElementById('btnSearch');
            const btnCause = document.getElementById('btnCause');
            if (btnSearch) {
                btnSearch.addEventListener('click', function(e) { e.preventDefault(); searchCase(); });
            }
            if (btnCause) {
                btnCause.addEventListener('click', function(e) { e.preventDefault(); getCauseList(); });
            }
        });
        document.getElementById('searchType').addEventListener('change', function() {
            const cnrForm = document.getElementById('cnrForm');
            const detailsForm = document.getElementById('detailsForm');
            
            if (this.value === 'cnr') {
                cnrForm.style.display = 'block';
                detailsForm.style.display = 'none';
            } else {
                cnrForm.style.display = 'none';
                detailsForm.style.display = 'block';
            }
        });

        async function searchCase() {
            const searchType = document.getElementById('searchType').value;
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '';
            
            let data = { search_type: searchType };
            
            if (searchType === 'cnr') {
                data.cnr = document.getElementById('cnr').value?.trim();
                if (!data.cnr) {
                    resultDiv.innerHTML = '<div class="result error"><h3>Error</h3><p>Please enter a CNR.</p></div>';
                    return;
                }
            } else {
                data.case_type = document.getElementById('caseType').value?.trim();
                data.case_number = document.getElementById('caseNumber').value?.trim();
                data.year = document.getElementById('year').value?.trim();
            }
            
            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    const text = await response.text();
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>Error</h3>
                            <p>Server error: ${response.status} ${response.statusText}</p>
                            <pre>${text}</pre>
                        </div>
                    `;
                    return;
                }

                const result = await response.json();
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <div class="result success">
                            <h3>Case Found!</h3>
                            <p><strong>Case Number:</strong> ${result.data.case_number || 'N/A'}</p>
                            <p><strong>Court:</strong> ${result.data.court_name || 'N/A'}</p>
                            <p><strong>Serial Number:</strong> ${result.data.serial_number || 'N/A'}</p>
                            <p><strong>Listed Today:</strong> ${result.data.is_listed_today ? 'Yes' : 'No'}</p>
                            <p><strong>Listed Tomorrow:</strong> ${result.data.is_listed_tomorrow ? 'Yes' : 'No'}</p>
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>Case Not Found</h3>
                            <p>${result.message || 'No matching case was found for the given input.'}</p>
                        </div>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="result error">
                        <h3>Error</h3>
                        <p>${error.message}</p>
                        <pre>${error.stack || ''}</pre>
                    </div>
                `;
            }
        }

        async function getCauseList() {
            const resultDiv = document.getElementById('result');
            
            try {
                const response = await fetch('/causelist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ court_code: '01' })
                });
                
                if (!response.ok) {
                    const text = await response.text();
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>Error</h3>
                            <p>Server error: ${response.status} ${response.statusText}</p>
                            <pre>${text}</pre>
                        </div>
                    `;
                    return;
                }

                const result = await response.json();
                
                if (result.success) {
                    let html = '<div class="result success"><h3>Cause List Retrieved!</h3>';
                    html += `<p>Found ${result.data.length} cases</p>`;
                    html += '<table border="1" style="width: 100%; border-collapse: collapse;">';
                    html += '<tr><th>Serial</th><th>Case Number</th><th>Time</th><th>Court Room</th></tr>';
                    
                    result.data.slice(0, 10).forEach(row => {
                        html += `<tr>
                            <td>${row.serial_number}</td>
                            <td>${row.case_number}</td>
                            <td>${row.time}</td>
                            <td>${row.court_room}</td>
                        </tr>`;
                    });
                    
                    html += '</table>';
                    if (result.filename) {
                        html += `<p><a href="/download/${result.filename}" target="_blank">Download CSV</a></p>`;
                    }
                    html += '</div>';
                    
                    resultDiv.innerHTML = html;
                } else {
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>Error</h3>
                            <p>${result.message || 'Could not fetch cause list'}</p>
                        </div>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="result error">
                        <h3>Error</h3>
                        <p>${error.message}</p>
                        <pre>${error.stack || ''}</pre>
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
    '''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
