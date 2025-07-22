import requests
from bs4 import BeautifulSoup
import json
import os
import re
from urllib.parse import urljoin
import time
import sys
from urllib.parse import urlparse

class DegreeScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def extract_courses(self, url):
        """Extract all courses with their hierarchical structure"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        structure = {
            'degree_title': '',
            'years': []
        }
        
        # Extract degree title
        title_elem = soup.find('h1', id='nombreTitulacion')
        if title_elem:
            structure['degree_title'] = title_elem.get_text(strip=True)

        
        # Find all subject tables
        tables = soup.find_all('table', class_='tabla_estandar')
        
        for table in tables:
            current_year = None
            current_semester = None
            
            rows = table.find_all('tr')
            
            for row in rows:
                # Detect year
                year_header = row.find('th', string=re.compile(r'CURSO|CUARTO|TERCER|SEGUNDO|PRIMER'))
                if year_header:
                    year_text = year_header.get_text(strip=True)
                    current_year = {
                        'name': year_text,
                        'semesters': []
                    }
                    structure['years'].append(current_year)
                    continue
                
                # Detect semester
                semester_header = row.find('td', string=re.compile(r'SEMESTRE|ANUALES'))
                if semester_header and current_year:
                    semester_text = semester_header.get_text(strip=True)
                    current_semester = {
                        'name': semester_text,
                        'subjects': []
                    }
                    current_year['semesters'].append(current_semester)
                    continue
                
                # Extract subject
                if current_semester:
                    self._extract_subject_from_row(row, current_semester)
        
        return structure
    
    def _extract_subject_from_row(self, row, semester):
        """Extract subject information from a table row"""
        cells = row.find_all('td')
        if len(cells) >= 4:
            code_cell, name_cell, type_cell, credits_cell = cells[0:4]
            
            # Extract PDF URL
            pdf_link = cells[-1].find('a') if len(cells) > 4 else None
            pdf_url = None
            if pdf_link and 'PDFGuiaPublica' in pdf_link.get('href', ''):
                pdf_url = urljoin(self.base_url, pdf_link['href'])
            
            subject = {
                'code': code_cell.get_text(strip=True),
                'name': name_cell.get_text(strip=True),
                'type': type_cell.get_text(strip=True),
                'credits': credits_cell.get_text(strip=True),
                'pdf_url': pdf_url
            }
            
            # Only add if it has a valid code
            if subject['code'] and len(subject['code']) > 3:
                semester['subjects'].append(subject)
    
    def download_pdfs(self, structure, output_dir='pdfs'):
        """Download all subject guide PDFs"""
        os.makedirs(output_dir, exist_ok=True)
        
        total_pdfs = 0
        for year in structure['years']:
            for semester in year['semesters']:
                for subject in semester['subjects']:
                    if subject['pdf_url']:
                        total_pdfs += 1
        
        print(f"Downloading {total_pdfs} PDFs...")
        
        downloaded = 0
        for year in structure['years']:
            for semester in year['semesters']:
                for subject in semester['subjects']:
                    if subject['pdf_url']:
                        filename = f"{subject['code']}_{subject['name'][:50]}"
                        filename = re.sub(r'[^\w\s-]', '', filename).strip()
                        filename = re.sub(r'[-\s]+', '-', filename)
                        filename = f"{filename}.pdf"
                        
                        filepath = os.path.join(output_dir, filename)
                        
                        try:
                            response = self.session.get(subject['pdf_url'])
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            downloaded += 1
                            print(f"✓ Downloaded: {filename} ({downloaded}/{total_pdfs})")
                            time.sleep(0.5)  # Be respectful to the server
                        except Exception as e:
                            print(f"✗ Error downloading {filename}: {e}")
        
        print(f"Download completed: {downloaded}/{total_pdfs} PDFs")
    
    def generate_report(self, structure, output_file='degree_structure.json'):
        """Generate JSON and plain text report"""
        # Save JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        # Save text report
        txt_file = output_file.replace('.json', '.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"DEGREE STRUCTURE: {structure['degree_title']}\n")
            f.write("=" * 60 + "\n\n")
            
            total_credits = 0
            total_subjects = 0
            
            for year in structure['years']:
                f.write(f"{year['name']}\n")
                f.write("-" * 40 + "\n")
                
                for semester in year['semesters']:
                    f.write(f"  {semester['name']}\n")
                    
                    for subject in semester['subjects']:
                        credits = subject['credits']
                        try:
                            total_credits += int(credits)
                        except:
                            pass
                        total_subjects += 1
                        
                        f.write(f"    • {subject['name']} ({subject['code']}) - "
                               f"{credits} credits - {subject['type']}\n")
                    f.write("\n")
                f.write("\n")
            
            f.write(f"SUMMARY:\n")
            f.write(f"Total subjects: {total_subjects}\n")
            f.write(f"Total credits: {total_credits}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python uned_scraper.py <DEGREE_URL>")
        sys.exit(1)
    url = sys.argv[1]
    
    # Extract base URL from the provided URL
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    scraper = DegreeScraper(base_url)
    
    print("Extracting degree structure...")
    structure = scraper.extract_courses(url)
    
    print("Generating reports...")
    scraper.generate_report(structure)
    
    print("Downloading PDFs...")
    scraper.download_pdfs(structure)
    
    print("✓ Process completed!")

if __name__ == "__main__":
    main()