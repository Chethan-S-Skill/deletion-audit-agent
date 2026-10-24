"""
Main orchestration for deletion audit agent
PhD-level solution for comprehensive deletion verification
"""
import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from identity_resolver import IdentityResolver
from evidence_analyzer import EvidenceAnalyzer
from audit_agent import AuditAgent
from report_generator import ReportGenerator

load_dotenv()

def main():
    print("="*70)
    print("DELETION AUDIT AGENT - Comprehensive Privacy Compliance System")
    print("="*70)

    # Setup paths
    dataset_dir = Path("dataset")
    evidence_dir = dataset_dir / "evidence"
    output_file = "output.csv"

    # Check if dataset exists
    if not dataset_dir.exists():
        print("ERROR: dataset/ folder not found!")
        print("Please download the dataset and place files in dataset/ folder")
        return

    # Load datasets
    print("\n[1/5] Loading datasets...")
    try:
        deletion_requests = pd.read_csv(dataset_dir / "deletion_requests.csv")
        user_identities = pd.read_csv(dataset_dir / "user_identities.csv")
        user_audit_log = pd.read_csv(dataset_dir / "user_audit_log.csv")
        system_activity = pd.read_csv(dataset_dir / "system_activity.csv")
        deletion_rules = pd.read_csv(dataset_dir / "deletion_rules.csv")
        evidence_files = pd.read_csv(dataset_dir / "evidence_files.csv")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Make sure all CSV files are in the dataset/ folder")
        return

    print(f"  - Loaded {len(deletion_requests)} deletion requests")
    print(f"  - Loaded {len(user_identities)} user identities")
    print(f"  - Loaded {len(user_audit_log)} audit log entries")
    print(f"  - Loaded {len(system_activity)} system activities")
    print(f"  - Loaded {len(evidence_files)} evidence files")

    # Initialize components
    print("\n[2/5] Initializing audit components...")
    identity_resolver = IdentityResolver(user_identities, user_audit_log)
    evidence_analyzer = EvidenceAnalyzer(evidence_files, evidence_dir)
    audit_agent = AuditAgent(deletion_rules, system_activity, identity_resolver, evidence_analyzer)
    report_generator = ReportGenerator()

    print("  - Identity Resolver: Ready")
    print("  - Evidence Analyzer: Ready")
    print("  - Audit Agent: Ready")

    # Process each deletion request
    print(f"\n[3/5] Processing {len(deletion_requests)} deletion requests...")
    print("-"*70)
    results = []

    # Option to test with smaller subset first
    # Uncomment the line below to test with first 10 cases:
    # deletion_requests = deletion_requests.head(10)

    for idx, request in deletion_requests.iterrows():
        case_id = request['case_id']

        # Show progress
        if idx % 50 == 0:
            print(f"Progress: {idx}/{len(deletion_requests)} cases processed ({idx/len(deletion_requests)*100:.1f}%)")

        try:
            # Run audit
            audit_result = audit_agent.audit_deletion(request)
            results.append(audit_result)

        except Exception as e:
            print(f"  WARNING: Error processing {case_id}: {e}")
            import traceback
            traceback.print_exc()
            # Add a fallback result
            results.append({
                'case_id': case_id,
                'deletion_status': 'INCOMPLETE',
                'steps_json': '[]'
            })

    print(f"Progress: {len(results)}/{len(deletion_requests)} cases processed (100.0%)")
    print("-"*70)

    # Generate output
    print(f"\n[4/5] Generating output files...")
    report_generator.generate_csv(results, output_file)
    print(f"  - Output saved: {output_file}")

    # Generate evaluation reports
    print("\n[5/5] Generating evaluation reports...")
    report_generator.generate_evaluation_report(results, "evaluation/evaluation_report.md")
    report_generator.generate_usage_report("evaluation/usage_report.md")
    print("  - Evaluation report: evaluation/evaluation_report.md")
    print("  - Usage report: evaluation/usage_report.md")

    # Summary statistics
    df = pd.DataFrame(results)
    print("\n" + "="*70)
    print("AUDIT COMPLETE - SUMMARY")
    print("="*70)
    print(f"Total Cases Processed: {len(results)}")
    print(f"  - COMPLETE:        {len(df[df['deletion_status'] == 'COMPLETE'])} cases")
    print(f"  - INCOMPLETE:      {len(df[df['deletion_status'] == 'INCOMPLETE'])} cases")
    print(f"  - NOT_APPLICABLE:  {len(df[df['deletion_status'] == 'NOT_APPLICABLE'])} cases")
    print("="*70)
    print(f"\nResults saved to: {output_file}")
    print("Evaluation reports saved to: evaluation/")
    print("\nReady for submission!")

if __name__ == "__main__":
    main()
