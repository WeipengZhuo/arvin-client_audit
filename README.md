# Client Conduct Auditor

Automated bulk assessment of client behavior for law firm termination decisions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## Overview

This tool processes client activity PDFs exported from case management systems (like MyCase) and:
1. **Extracts** timeline events, communications, and case metadata
2. **Analyzes** client behavior using Claude AI and SOP classifications
3. **Generates** a formatted Excel spreadsheet with termination recommendations

## Features

- ✅ **Batch PDF Processing** - Handle dozens of client cases at once
- ✅ **SOP-Compliant Classification** - Normal / Special / E-Special / Delinquent
- ✅ **Automated Recommendations** - Continue / Cure / Terminate / Executive Review
- ✅ **Firm Fault Detection** - Identifies potential malpractice or ethics issues
- ✅ **Formatted Spreadsheet** - Color-coded, professional deliverable
- ✅ **Summary Dashboard** - Statistics and breakdown by category

## Installation

### Requirements

- Python 3.8+
- Anthropic API key

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/arvin-client_audit.git
cd arvin-client_audit

# Run installation script
bash install.sh

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or install manually:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python auditor.py /path/to/pdf_folder
```

This will:
- Process all PDFs in the folder
- Generate `client_assessment.xlsx` in current directory

### Custom Output Path

```bash
python auditor.py /path/to/pdf_folder -o ~/Desktop/assessment.xlsx
```

### With Custom SOP File

```bash
python auditor.py /path/to/pdf_folder --sop /path/to/custom_sop.md
```

### Full Example

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Process PDFs
python auditor.py ~/Downloads/delinquent_clients -o ~/Desktop/february_audit.xlsx

# Output:
# ✅ Successfully extracted data from 15 PDFs
# 🤖 Analyzing 15 cases...
# ✅ Spreadsheet saved: ~/Desktop/february_audit.xlsx
```

## Input Format

### Expected PDF Structure

PDFs should be **MyCase exports** containing:
- **Items/Info section** - Case metadata (client name, case #, attorney)
- **Activities & Timeline** - Full chronological history

Supported export types:
- `Activities & Timeline` (full export, NOT filtered by date)
- `Items / Info`
- Combined exports

### Naming Convention (Optional)

PDFs can be named anything, but descriptive names help:
```
01_doe_john_asylum.pdf
02_smith_maria_green_card.pdf
03_garcia_family_deportation.pdf
```

## Output Format

### Spreadsheet Columns

| Column | Description |
|--------|-------------|
| **Case Name** | Client name extracted from PDF |
| **PDF Source** | Original filename for reference |
| **Client Classification** | Normal / Special / E-Special / Delinquent / Delinquent + Special |
| **Type of Notice Sent** | Notice to Cure / Notice of Termination / None sent |
| **Firm Fault** | Yes / No / Unclear from records |
| **Firm Fault Explanation** | Brief explanation if firm made error |
| **Current Status** | Active / Pending Cure / Terminated / Recommended for Termination |
| **Recommendation** | Continue / Cure / Terminate / Executive Review |
| **Reasoning** | 2-3 sentence explanation with evidence |
| **Key Evidence** | Specific quotes from timeline supporting classification |

### Color Coding

- 🟢 **Green** - Continue representation
- 🟡 **Yellow** - Send Notice to Cure
- 🔴 **Red** - Proceed with Termination
- 🔵 **Blue** - Executive Review Required

### Summary Sheet

Includes:
- Total cases analyzed
- Classification breakdown (Special vs E-Special vs Delinquent)
- Recommendation statistics
- Firm fault analysis

## SOP Classifications

### Normal Client
✅ Pays on time, communicates respectfully, stays within scope

### Special Client
⚠️ Difficult but salvageable:
- Excessive contact seeking reassurance
- Expressions of dissatisfaction
- Scope expansion attempts
- **Key:** Still respectful, no abuse

### E-Special Client (Excessively Special)
🚫 Shocks the conscience - automatic termination track:
- Yelling, screaming, profanity
- Threats (lawsuit, State Bar, physical harm)
- Accusations of fraud/theft
- Hostile office conduct
- Review blackmail

### Delinquent
💰 Any past-due balance per MyCase

### Delinquent + Special
⚠️💰 Combination requiring dual assessment

## How It Works

### Phase 1: PDF Extraction (`pdf_extractor.py`)

- Uses `pdfplumber` to extract text from all pages
- Parses timeline events with dates, actors, content
- Extracts metadata (case number, attorney, status)
- Prioritizes communication snippets with emotional language

### Phase 2: Behavior Analysis (`behavior_classifier.py`)

- Sends case data + SOP to Claude API (Sonnet 4)
- Claude analyzes behavior against SOP definitions
- Returns structured classification and recommendation
- Includes specific evidence quotes from timeline

### Phase 3: Spreadsheet Generation (`spreadsheet_generator.py`)

- Creates formatted Excel workbook with `openpyxl`
- Applies color coding based on recommendations
- Generates summary statistics sheet
- Auto-adjusts column widths for readability

## Advanced Options

### Verbose Mode

```bash
python auditor.py /path/to/pdfs --verbose
```

Shows detailed progress and full error tracebacks.

### API Key Management

Three ways to provide your API key:

1. **Environment variable** (recommended):
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

2. **Command-line argument**:
   ```bash
   python auditor.py /path/to/pdfs --api-key "sk-ant-..."
   ```

3. **Hardcode in `behavior_classifier.py`** (not recommended for security)

## Troubleshooting

### "No PDF files found"
- Ensure folder contains `.pdf` files
- Check folder path is correct
- PDFs must have `.pdf` extension

### "ANTHROPIC_API_KEY not found"
- Set environment variable: `export ANTHROPIC_API_KEY="sk-ant-..."`
- Or pass via `--api-key` flag

### "Cannot extract case name"
- Plugin will use filename as fallback
- Ensure PDFs are MyCase exports (not scanned images)

### "Error during analysis"
- Check API key is valid
- Ensure internet connection
- Review verbose output: `python auditor.py /path/to/pdfs -v`

### Partial Results
If some PDFs fail, the tool continues processing others. Check console output for errors.

## Limitations

- **Scanned PDFs**: Plugin requires machine-readable text, not scanned images
- **OCR**: If PDFs are scanned, use OCR tool first (Adobe Acrobat, Tesseract)
- **Token Limits**: Very large PDFs (>100 pages) may be truncated
- **Rate Limits**: Processing 50+ cases may hit API rate limits (add delays if needed)

## Best Practices

### For Best Results

1. **Export full timeline** - Don't filter by date in MyCase
2. **Include all related cases** - Client may have multiple matters
3. **Fresh exports** - Use recent MyCase data
4. **Review results** - AI recommendations should be reviewed by QA/attorney

### Workflow Integration

```
Step 1: Export PDFs from MyCase
  ↓
Step 2: Run auditor.py (this plugin)
  ↓
Step 3: Review spreadsheet
  ↓
Step 4: QA review (Susan La Valley)
  ↓
Step 5: Executive approval (COO/CEO)
  ↓
Step 6: Execute recommendations
```

## Support

### Issues
- Check README troubleshooting section
- Review verbose output: `python auditor.py /path/to/pdfs -v`

### Customization
Plugin is modular - each component can be modified:
- `pdf_extractor.py` - Change extraction logic
- `behavior_classifier.py` - Adjust classification rules
- `spreadsheet_generator.py` - Modify output format

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Version History

- **v1.0.0** (2026-02-10) - Initial release
  - Batch PDF processing
  - SOP-compliant classification
  - Formatted Excel output
  - Summary statistics

## Credits

Built with:
- [Claude API](https://anthropic.com) - Behavior analysis
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF extraction
- [openpyxl](https://openpyxl.readthedocs.io) - Excel generation
