# 🚀 Quick Start Guide

## Step 1: Download Dataset

Go to the hackathon repository and download the dataset:
https://github.com/interviewstreet/hackerrank-orchestrate-october26

Place all files in the `dataset/` folder:
```
dataset/
  ├── deletion_requests.csv
  ├── user_identities.csv
  ├── user_audit_log.csv
  ├── system_activity.csv
  ├── deletion_rules.csv
  ├── evidence_files.csv
  └── evidence/
      └── (all evidence files)
```

## Step 2: Setup Environment

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up API key**:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API key
# Get a free key from: https://console.anthropic.com/
```

## Step 3: Run the Audit

```bash
python src/main.py
```

The script will:
- ✅ Load all 518 deletion requests
- 🔍 Analyze each case for remaining data
- 📊 Generate `output.csv` with results
- 📈 Create evaluation reports

## Step 4: Submit

Your submission should include:
1. ✅ `output.csv` (518 rows)
2. ✅ `evaluation/evaluation_report.md`
3. ✅ `evaluation/usage_report.md`
4. ✅ `code.zip` (all source code + README)
5. ✅ Chat transcript

## What the Code Does

### 1. Identity Resolution (`identity_resolver.py`)
- Finds ALL identities for a user (current + historical)
- Tracks email changes, username changes, phone changes
- Handles user merges

### 2. Evidence Analysis (`evidence_analyzer.py`)
- Searches through evidence files for user data
- Checks PDFs, logs, JSON files, database snapshots
- Identifies which system/resource contains the data

### 3. Audit Logic (`audit_agent.py`)
- **COMPLETE**: All data deleted, no restore risks
- **INCOMPLETE**: Data still exists somewhere
- **NOT_APPLICABLE**: User never existed

### 4. Step Generation
For each case, generates JSON steps:
- **FINDING**: What data exists, where it is
- **REMEDIATION**: How to delete it
- **VERIFICATION**: How to confirm deletion

## Expected Output Format

```csv
case_id,deletion_status,steps_json
DEL001,COMPLETE,"[{\"step_no\":1,\"phase\":\"FINDING\",...}]"
DEL002,INCOMPLETE,"[{\"step_no\":1,\"phase\":\"FINDING\",...}]"
DEL003,NOT_APPLICABLE,"[]"
```

## Troubleshooting

### "dataset/ folder not found"
Make sure you've downloaded and extracted the dataset to the `dataset/` folder

### "ANTHROPIC_API_KEY not set"
Create a `.env` file with your API key (copy from `.env.example`)

### Running slowly
The full audit takes ~20-30 minutes for 518 cases. You can test with a subset first by modifying `main.py`

## Tips for the Hackathon

1. **Test with small subset first**: Modify line in `main.py` to process only first 10 cases
2. **Check intermediate results**: Print statements show progress
3. **Validate output format**: Make sure CSV has exactly 518 rows
4. **Review sample cases**: Look at evaluation report to verify logic

## Next Steps

1. Download the dataset
2. Run the code
3. Review the output
4. Refine the audit logic based on actual data patterns
5. Package everything for submission

Good luck! 🎉
