# UNED Degree Scraper

A Python web scraper designed to extract and organize academic information from UNED (Universidad Nacional de Educación a Distancia) degree program pages. This tool automatically downloads course structures, subject information, and PDF guides for comprehensive academic planning.

## Features

- 🎓 **Complete Degree Structure Extraction**: Automatically parses degree programs organized by years and semesters
- 📚 **Subject Information**: Extracts course codes, names, credits, and academic types
- 📄 **PDF Guide Downloads**: Bulk downloads all subject guide PDFs for offline reference
- 📊 **Multiple Output Formats**: Generates both JSON (machine-readable) and TXT (human-readable) reports
- 🔄 **Hierarchical Organization**: Maintains the original academic structure (Year → Semester → Subject)
- ⚡ **Respectful Scraping**: Implements delays to avoid overwhelming the server

## Requirements

- Python 3.6+
- Internet connection
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/devmunoz/uned-degree-scraper.git
   cd uned-degree-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the scraper with a UNED degree URL:

```bash
python uned_scraper.py "https://www.uned.es/universidad/inicio/estudios/grados/grado-en-ingenieria-informatica.html?idContenido=5"
```

### Example URLs

- **Computer Engineering**: `https://www.uned.es/universidad/inicio/estudios/grados/grado-en-ingenieria-informatica.html?idContenido=5`
- **Psychology**: `https://www.uned.es/universidad/inicio/estudios/grados/grado-en-psicologia.html?idContenido=5`
- **Business Administration**: `https://www.uned.es/universidad/inicio/estudios/grados/grado-en-administracion-y-direccion-de-empresas.html?idContenido=5`

## Output Files

The scraper generates the following files:

### 1. `degree_structure.json`
Structured JSON data containing the complete degree information:
```json
{
  "degree_title": "Grado en Ingeniería Informática",
  "years": [
    {
      "name": "PRIMER CURSO",
      "semesters": [
        {
          "name": "SEMESTRE 1",
          "subjects": [
            {
              "code": "71011013",
              "name": "FUNDAMENTOS FÍSICOS DE LA INFORMÁTICA",
              "type": "Formación Básica",
              "credits": "6",
              "pdf_url": "https://www.uned.es/universidad/pdf/..."
            }
          ]
        }
      ]
    }
  ]
}
```

### 2. `degree_structure.txt`
Human-readable text report with summary statistics:
```
DEGREE STRUCTURE: Grado en Ingeniería Informática
============================================================

PRIMER CURSO
----------------------------------------
  SEMESTRE 1
    • FUNDAMENTOS FÍSICOS DE LA INFORMÁTICA (71011013) - 6 credits - Formación Básica

SUMMARY:
Total subjects: 40
Total credits: 240
```

### 3. `pdfs/` Directory
Contains all downloaded PDF guides organized by subject code and name:
```
pdfs/
├── 71011013_FUNDAMENTOS-FÍSICOS-DE-LA-INFORMÁTICA.pdf
├── 71901020_FUNDAMENTOS-DE-PROGRAMACIÓN.pdf
└── ...
```

<details>
<summary>Technical Details</summary>

## Code Structure

### Main Classes

- **`DegreeScraper`**: Main class that handles all scraping operations
    - `extract_courses()`: Parses HTML and extracts degree structure
    - `download_pdfs()`: Downloads all subject guide PDFs
    - `generate_report()`: Creates JSON and text output files

### Key Methods

- **HTML Parsing**: Uses BeautifulSoup to navigate complex table structures
- **Data Extraction**: Identifies years, semesters, and subjects using regex patterns
- **File Management**: Automatically creates directories and handles file naming
- **Error Handling**: Gracefully handles network errors and missing data

## Configuration

### Custom Headers
The scraper uses a standard browser User-Agent to avoid blocking:
```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

### Download Delays
Implements a 0.5-second delay between PDF downloads to be respectful to the server.


## Troubleshooting


### Common Issues

1. **Network Errors**:
   - Check your internet connection
   - Verify the URL is accessible
   - Some PDFs might be temporarily unavailable

2. **Missing Dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Permission Errors**:
   - Ensure write permissions in the current directory
   - Run with appropriate user privileges

4. **Empty Results**:
   - Verify the URL contains course information
   - Check if the page structure has changed

### Debug Mode
For troubleshooting, you can modify the code to add more verbose logging or inspect the HTML structure.

</details>

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Legal Considerations

- This tool is for educational and research purposes
- Respect UNED's terms of service and robots.txt
- Use responsibly and avoid overwhelming their servers
- Downloaded content is subject to UNED's copyright policies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for students and researchers working with UNED academic programs
- Uses web scraping best practices to minimize server impact
- Inspired by the need for organized academic planning tools

## Support

If you encounter issues or have suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contribute improvements via pull requests

---

**Note**: This scraper is designed specifically for UNED's current website structure. If the website changes, the scraper may need updates to function properly.
