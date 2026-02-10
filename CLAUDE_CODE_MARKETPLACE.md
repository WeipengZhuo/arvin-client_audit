# Claude Code Marketplace Plugin Guide

Complete guide for creating and using Claude Code marketplace plugins.

---

## ✅ What Was Created

Your repository is now a **Claude Code Marketplace Plugin** that can be installed and used directly in Claude Code!

### Repository Structure

```
arvin-client_audit/
├── .claude-plugin/
│   ├── plugin.json           # Plugin metadata
│   └── marketplace.json      # Marketplace catalog
├── commands/
│   ├── audit-clients.md      # /audit-clients command
│   └── setup-auditor.md      # /setup-auditor command
├── [tool files...]           # Python scripts
└── README.md                 # Updated with plugin install instructions
```

---

## 🚀 How to Install Your Plugin in Claude Code

### Method 1: Install from GitHub (Public Marketplace)

In Claude Code, run these commands:

```
/plugin marketplace add WeipengZhuo/arvin-client_audit
```

This adds your marketplace. Then browse and install:

```
/plugin install client-conduct-auditor
```

Or use the UI:
1. Type `/plugin`
2. Click "Discover"
3. Find "client-conduct-auditor"
4. Click "Install"

### Method 2: Install from Local Directory

If testing locally:

```
/plugin marketplace add file:///Users/weipengzhuo/Insight-Expansion/arvin-client_audit
/plugin install client-conduct-auditor
```

---

## 📝 Available Commands

Once installed, you have two new slash commands:

### `/setup-auditor`
**Purpose:** First-time setup and testing

**What it does:**
- Checks if Python dependencies are installed
- Verifies API key is set
- Generates sample test PDFs
- Runs a test audit
- Confirms everything works

**Example:**
```
/setup-auditor
```

Claude will:
- Install dependencies if needed
- Guide you to set API key
- Run a test with 7 sample cases
- Show you the output spreadsheet

---

### `/audit-clients <folder>`
**Purpose:** Process real client PDFs

**What it does:**
- Validates folder exists and contains PDFs
- Runs the Python auditor tool
- Shows progress in Claude Code
- Generates Excel spreadsheet
- Summarizes recommendations

**Example:**
```
/audit-clients ~/Downloads/february_clients
```

Claude will:
- Extract data from all PDFs
- Analyze using Claude API
- Generate `client_assessment.xlsx`
- Show summary: X cases to continue, Y to terminate, etc.

**With custom output:**
```
/audit-clients ~/Downloads/pdfs -o ~/Desktop/audit.xlsx
```

---

## 🏗️ How Claude Code Plugins Work

### Plugin Structure

```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "client-conduct-auditor",
  "version": "1.0.0",
  "description": "Tool description",
  "commands": ["audit-clients", "setup-auditor"]
}
```

### Marketplace Structure

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "arvin-client-audit-marketplace",
  "plugins": [
    {
      "name": "client-conduct-auditor",
      "source": ".",
      "category": "productivity"
    }
  ]
}
```

### Commands (Markdown Files)

Each command is a markdown file in `commands/` directory:

```markdown
# Command Name

Description

## Usage
`/command-name <args>`

## Your Task
When user runs this command:
1. Do X
2. Do Y
3. Do Z
```

Claude Code reads these and knows how to execute your tool!

---

## 🔍 How It Actually Works

When a user types `/audit-clients ~/Downloads/pdfs`:

1. **Claude Code reads** `commands/audit-clients.md`
2. **Claude sees instructions** like "Run python3 auditor.py..."
3. **Claude executes** the Python script via Bash tool
4. **Claude monitors** the output and shows progress
5. **Claude summarizes** results for the user

**It's like giving Claude a recipe** for how to use your tool!

---

## 📦 Creating Your Own Marketplace Plugins

### Step 1: Create Plugin Structure

```bash
mkdir -p .claude-plugin commands
```

### Step 2: Create plugin.json

```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "What your plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "commands": ["command1", "command2"]
}
```

### Step 3: Create marketplace.json

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "your-marketplace-name",
  "version": "1.0.0",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "your-plugin-name",
      "description": "Plugin description",
      "source": ".",
      "category": "productivity"
    }
  ]
}
```

### Step 4: Create Command Files

In `commands/your-command.md`:

```markdown
# Your Command Name

What this command does

## Usage
`/your-command <args>`

## Your Task
When the user runs this command:

1. **Do something:**
   ```bash
   some-cli-tool --arg value
   ```

2. **Show results:**
   Tell user what happened

3. **Handle errors:**
   If X fails, do Y
```

### Step 5: Push to GitHub

```bash
git add -A
git commit -m "feat: add Claude Code plugin support"
git push
```

### Step 6: Install and Test

```
/plugin marketplace add your-username/your-repo
/plugin install your-plugin-name
/your-command
```

---

## 🎯 Best Practices

### 1. Clear Instructions in Commands
Commands should tell Claude **exactly** what to do:
- ✅ "Run `python3 script.py <folder>`"
- ❌ "Process the files somehow"

### 2. Error Handling
Include fallbacks:
```markdown
## Error Handling

If API key not set:
```bash
export API_KEY="..."
```

If dependencies missing:
```bash
pip install -r requirements.txt
```
```

### 3. Progress Updates
Tell Claude to show progress:
```markdown
1. Tell user: "Processing 15 PDFs..."
2. Show the output from the tool
3. Summarize: "✅ Generated spreadsheet"
```

### 4. Categories

Choose the right category:
- `development` - Coding tools
- `productivity` - Workflow tools
- `learning` - Educational
- `security` - Security tools

### 5. Versioning

Use semantic versioning:
- `1.0.0` - Initial release
- `1.1.0` - New features
- `1.0.1` - Bug fixes

---

## 🔧 Advanced: Multiple Plugins in One Marketplace

You can host multiple plugins:

```json
{
  "plugins": [
    {
      "name": "plugin-1",
      "source": "./plugins/plugin-1"
    },
    {
      "name": "plugin-2",
      "source": "./plugins/plugin-2"
    }
  ]
}
```

Directory structure:
```
your-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── plugin-1/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── commands/
│   └── plugin-2/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── commands/
```

---

## 📚 Real-World Examples

### Example 1: Git Helper Plugin

```markdown
# Commit with AI Message

## Usage
`/smart-commit`

## Your Task
1. Run `git status` to see changes
2. Run `git diff` to see details
3. Generate a commit message based on the changes
4. Ask user: "Commit with this message? [y/n]"
5. If yes, run `git commit -m "..."`
```

### Example 2: Database Query Plugin

```markdown
# Query Database

## Usage
`/db-query <sql>`

## Your Task
1. Validate SQL is safe (no DROP, DELETE without WHERE)
2. Run: `psql -d mydb -c "<sql>"`
3. Format results as table
4. If error, explain what went wrong
```

### Example 3: Screenshot Analyzer

```markdown
# Analyze Screenshot

## Usage
`/analyze-screenshot <path>`

## Your Task
1. Read the image file
2. Analyze the screenshot (you can see images!)
3. Describe what's shown
4. Suggest improvements if it's a UI
```

---

## 🌐 Sharing Your Marketplace

### Public Marketplace (GitHub)

1. **Push to GitHub** (you already did this!)
2. **Share the install command:**
   ```
   /plugin marketplace add WeipengZhuo/arvin-client_audit
   ```

3. **Add to README:**
   ```markdown
   ## Installation

   In Claude Code:
   ```
   /plugin marketplace add WeipengZhuo/arvin-client_audit
   /plugin install client-conduct-auditor
   ```
   ```

### Private Marketplace (GitHub Private Repo)

Same as public, but users need GitHub access token:

```bash
export GITHUB_TOKEN="ghp_..."
```

Then:
```
/plugin marketplace add your-username/private-repo
```

### Internal Team Marketplace

Host on company GitLab/Bitbucket:

```
/plugin marketplace add https://gitlab.company.com/team/plugins.git
```

---

## 🎓 What You Learned

1. **Claude Code plugins** are Git repos with `.claude-plugin/` directory
2. **Commands** are markdown files telling Claude how to use your tools
3. **Marketplaces** catalog multiple plugins for distribution
4. **Installation** is via `/plugin marketplace add` + `/plugin install`
5. **Your tool** is now a proper Claude Code plugin!

---

## 🚀 Next Steps

### For Your Plugin

1. **Test it:**
   ```
   /plugin marketplace add WeipengZhuo/arvin-client_audit
   /plugin install client-conduct-auditor
   /setup-auditor
   ```

2. **Use it:**
   ```
   /audit-clients ~/Downloads/client_pdfs
   ```

3. **Share it:**
   - Tell Arvin and the team
   - Share on legal tech forums
   - Submit to official Anthropic marketplace

### For Future Plugins

Create more tools:
- Contract analyzer
- Billing time tracker
- Case deadline reminder
- Client communication logger

Each can be a new plugin in your marketplace!

---

## 📖 Resources

- **Official Docs:** https://code.claude.com/docs/en/plugin-marketplaces
- **Plugin Schema:** https://anthropic.com/claude-code/plugin.schema.json
- **Official Plugins:** https://github.com/anthropics/claude-plugins-official
- **Your Plugin:** https://github.com/WeipengZhuo/arvin-client_audit

---

## ✅ Summary

You now have a **public Claude Code marketplace plugin** that:

✅ Can be installed with 2 commands
✅ Provides `/setup-auditor` and `/audit-clients` slash commands
✅ Works directly in Claude Code interface
✅ Is hosted on GitHub and publicly accessible
✅ Follows official Anthropic plugin standards

**Try it now:**
```
/plugin marketplace add WeipengZhuo/arvin-client_audit
/plugin install client-conduct-auditor
/setup-auditor
```
