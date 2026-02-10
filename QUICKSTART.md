# Quick Start Guide

Get up and running with Client Conduct Auditor in 5 minutes.

## Step 1: Install

```bash
cd .claude/plugins/client-conduct-auditor
bash install.sh
```

## Step 2: Set API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

Or add to your shell profile for persistence:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Step 3: Prepare Your PDFs

1. **In MyCase**, for each client case:
   - Go to the case
   - Navigate to **Activities & Timeline**
   - Click **Export** → Select **All** (not filtered by date)
   - Save as PDF

2. **Place all PDFs** in a folder:
   ```
   ~/Downloads/client_audits/
   ├── case_001_john_doe.pdf
   ├── case_002_maria_smith.pdf
   ├── case_003_garcia_family.pdf
   └── ...
   ```

## Step 4: Run the Audit

```bash
python3 auditor.py ~/Downloads/client_audits
```

**Output:**
```
╔══════════════════════════════════════════════════════════════╗
║         CLIENT CONDUCT AUDITOR v1.0                          ║
╚══════════════════════════════════════════════════════════════╝

📁 PDF folder: /Users/you/Downloads/client_audits
📄 Found 15 PDF files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Extracting data from PDFs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Extracting: case_001_john_doe.pdf
Extracting: case_002_maria_smith.pdf
...

✅ Successfully extracted data from 15 PDFs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Analyzing client behavior using Claude API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Starting batch analysis...

Analyzing 1/15: John Doe
Analyzing 2/15: Maria Smith
...

✅ Completed analysis of 15 cases

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Generating assessment spreadsheet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Spreadsheet saved: ./client_assessment.xlsx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
  • Continue representation: 8 cases
  • Send Notice to Cure: 4 cases
  • Proceed with Termination: 2 cases
  • Executive Review Required: 1 cases

📊 Output saved to: ./client_assessment.xlsx

✅ Audit complete!
```

## Step 5: Review Results

Open `client_assessment.xlsx` in Excel or Google Sheets.

### Main Sheet: Client Assessments

| Case Name | Classification | Recommendation | Reasoning |
|-----------|----------------|----------------|-----------|
| John Doe | Special | Send Notice to Cure | Client has called 3x/day for updates but remains respectful... |
| Maria Smith | E-Special | Proceed with Termination | Client yelled at paralegal, used profanity, threatened State Bar... |
| Garcia Family | Delinquent | Continue representation | Past due by $500 but payment plan in place... |

**Color coding:**
- 🟢 Green = Continue
- 🟡 Yellow = Cure
- 🔴 Red = Terminate
- 🔵 Blue = Executive Review

### Summary Sheet

Statistics dashboard showing:
- Total cases analyzed
- Classification breakdown
- Recommendation counts
- Firm fault analysis

## Common Options

### Custom Output Location

```bash
python3 auditor.py ~/Downloads/client_audits -o ~/Desktop/february_audit.xlsx
```

### Use Different SOP

```bash
python3 auditor.py ~/Downloads/client_audits --sop /path/to/custom_sop.md
```

### Verbose Mode (for debugging)

```bash
python3 auditor.py ~/Downloads/client_audits --verbose
```

### Help

```bash
python3 auditor.py --help
```

## What the Plugin Does

1. **📄 Extracts** text from each PDF:
   - Case name, case number, dates
   - Timeline events with dates
   - Communications and notes
   - Metadata (attorney, status, etc.)

2. **🤖 Analyzes** behavior using Claude AI:
   - Compares timeline events to SOP definitions
   - Identifies Special vs E-Special conduct
   - Detects patterns of abuse or legitimate grievances
   - Checks for firm fault

3. **📊 Generates** formatted spreadsheet:
   - All required columns per your spec
   - Color-coded recommendations
   - Summary statistics
   - Ready for QA review

## Next Steps

After generating the spreadsheet:

1. **Review results** - AI provides recommendations, but human review is essential
2. **QA approval** - Susan La Valley reviews per SOP Section 8.2
3. **Executive review** - Cases requiring termination go to COO/CEO
4. **Execute** - Follow SOP protocols for notices, locks, termination

## Tips for Best Results

### ✅ Do This

- Export **full timeline** from MyCase (not date-filtered)
- Include **all related cases** for each client
- Use **recent exports** (within last week)
- Review **AI reasoning** - it cites specific evidence
- Process cases in **batches of 20-30** to avoid rate limits

### ❌ Avoid This

- Scanned PDFs (must be machine-readable text)
- Partial timeline exports
- Screenshots instead of PDF exports
- Very old data (>6 months stale)

## Troubleshooting

### No PDFs Found

```bash
❌ Error: No PDF files found in: /path/to/folder
```

**Fix:** Ensure folder contains `.pdf` files with correct extension.

### API Key Not Set

```bash
❌ Error: ANTHROPIC_API_KEY not found
```

**Fix:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### SOP File Not Found

```bash
❌ Error: SOP file not found: /Users/.../special delinquent sop.md
```

**Fix:** Either:
- Move SOP to default location: `~/Downloads/special delinquent sop.md`
- Or use custom path: `python3 auditor.py /path/to/pdfs --sop /custom/path.md`

### PDF Extraction Errors

```bash
Error extracting case_003.pdf: Cannot extract text
```

**Possible causes:**
- PDF is scanned image (needs OCR)
- PDF is corrupted
- PDF is password-protected

**Fix:**
- Use Adobe Acrobat to OCR scanned documents
- Re-export from MyCase
- Tool continues with other files - check output for partial results

## Support

For issues:
1. Check this guide
2. Run with `--verbose` flag
3. Review console output for errors

For customization:
- Modify extraction: `pdf_extractor.py`
- Adjust classification: `behavior_classifier.py`
- Change output format: `spreadsheet_generator.py`

---

**Ready to process your client cases?**

```bash
python3 auditor.py /path/to/your/pdfs
```
