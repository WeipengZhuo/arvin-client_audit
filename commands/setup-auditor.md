# Setup Client Conduct Auditor

Install and configure the Client Conduct Auditor tool.

## Usage

`/setup-auditor`

## What This Does

Sets up the Client Conduct Auditor so you can use `/audit-clients` command.

## Your Task

When the user runs this command:

1. **Navigate to repository:**
   ```bash
   cd /Users/weipengzhuo/Insight-Expansion/arvin-client_audit
   ```

2. **Check current status:**
   ```bash
   # Check if dependencies installed
   python3 -c "import anthropic, pdfplumber, openpyxl" 2>/dev/null && echo "✅ Dependencies installed" || echo "❌ Dependencies missing"

   # Check API key
   if [ -n "$ANTHROPIC_API_KEY" ]; then echo "✅ API key set"; else echo "❌ API key not set"; fi

   # Check SOP file
   if [ -f "/Users/weipengzhuo/Downloads/special delinquent sop.md" ]; then echo "✅ SOP file found"; else echo "⚠️  SOP file not at default location"; fi
   ```

3. **Install if needed:**
   ```bash
   bash install.sh
   ```

4. **Guide API key setup if needed:**
   If ANTHROPIC_API_KEY not set, tell user:
   ```
   To set your API key, run:

   export ANTHROPIC_API_KEY="sk-ant-your-key-here"

   Or add to shell profile for persistence:

   echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
   source ~/.zshrc
   ```

5. **Test with sample data:**
   ```bash
   python3 test_data_generator.py
   python3 auditor.py ./test_pdfs -o ./test_assessment.xlsx
   ```

6. **Confirm success:**
   ```
   ✅ Client Conduct Auditor is ready!

   Test output saved: ./test_assessment.xlsx

   Usage:
     /audit-clients /path/to/pdf_folder

   Documentation:
     - README.md: Full guide
     - QUICKSTART.md: 5-minute setup
     - IMPLEMENTATION_SUMMARY.md: Technical details
   ```

## Example Output

```
User: /setup-auditor

You:
🔍 Checking Client Conduct Auditor status...

❌ Dependencies missing
✅ API key set
✅ SOP file found

Installing dependencies...
✅ Dependencies installed

Generating test data...
✅ Created 7 sample PDFs

Running test audit...
✅ Processed 7 cases
✅ Test spreadsheet: ./test_assessment.xlsx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Client Conduct Auditor is ready!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Usage:
  /audit-clients ~/Downloads/client_pdfs

Documentation:
  Open README.md for full usage guide
```

## Troubleshooting

**Python not found:**
```bash
# Install Python 3.8+
brew install python3  # macOS
```

**Permission denied on install.sh:**
```bash
chmod +x install.sh
bash install.sh
```

**Import errors after install:**
```bash
# Reinstall dependencies
pip3 install --upgrade -r requirements.txt
```
