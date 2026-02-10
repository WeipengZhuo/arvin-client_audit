# Audit Client Conduct

Process client activity PDFs and generate termination recommendations using AI-powered behavior analysis.

## Usage

`/audit-clients <pdf_folder_path> [output_path]`

## What This Does

1. Extracts data from all MyCase PDF exports in the folder
2. Analyzes each case using Claude API + client behavior SOP
3. Generates formatted Excel spreadsheet with:
   - Client classifications (Normal/Special/E-Special/Delinquent)
   - Termination recommendations
   - Firm fault assessment
   - Evidence-based reasoning

## Your Task

When the user runs this command:

1. **Get the repository path:**
   ```bash
   REPO_PATH="/Users/weipengzhuo/Insight-Expansion/arvin-client_audit"
   ```

2. **Validate inputs:**
   - Check that `pdf_folder_path` exists and contains PDF files
   - Use default output path `./client_assessment.xlsx` if not specified
   - Verify ANTHROPIC_API_KEY environment variable is set

3. **Run the auditor:**
   ```bash
   cd "$REPO_PATH"
   python3 auditor.py <pdf_folder_path> -o <output_path>
   ```

4. **Monitor progress:**
   - Show the auditor's progress output to user
   - Report any errors encountered
   - Confirm when spreadsheet is generated

5. **Summarize results:**
   - Tell user where spreadsheet was saved
   - Provide high-level summary of recommendations (how many Continue/Cure/Terminate/Review)
   - Suggest next steps (open spreadsheet, QA review, etc.)

## Example

```
User: /audit-clients ~/Downloads/delinquent_clients

You:
✅ Found 15 PDFs in ~/Downloads/delinquent_clients
🤖 Running Client Conduct Auditor...

[shows progress output from tool]

✅ Assessment complete!
📊 Spreadsheet saved: ./client_assessment.xlsx

Summary:
  • Continue representation: 8 cases
  • Send Notice to Cure: 4 cases
  • Proceed with Termination: 2 cases
  • Executive Review Required: 1 case

Next steps:
1. Open the spreadsheet to review details
2. Have QA review recommendations
3. Executive approval for terminations
```

## Prerequisites

- Client Conduct Auditor installed
- ANTHROPIC_API_KEY environment variable set
- MyCase PDF exports in specified folder

## Error Handling

If prerequisites aren't met, guide user:

**Missing API Key:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Dependencies not installed:**
```bash
cd /Users/weipengzhuo/Insight-Expansion/arvin-client_audit
bash install.sh
```

**No PDFs found:**
- Verify folder path is correct
- Check that files have .pdf extension
- Ensure PDFs are MyCase exports (not scanned images)
