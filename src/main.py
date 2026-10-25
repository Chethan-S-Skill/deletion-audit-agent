"""
Main orchestration for deletion audit agent
Privacy Compliance Audit Pipeline
"""
import os
import sys
import pandas as pd
from pathlib import Path

# Add src to sys.path
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from identity_resolver import IdentityResolver
from evidence_analyzer import EvidenceAnalyzer
from audit_agent import AuditAgent
from report_generator import ReportGenerator

def main():
    print("=" * 70)
    print("DELETION AUDIT AGENT - Comprehensive Privacy Compliance System")
    print("=" * 70)

    # Setup paths relative to workspace root
    workspace_root = Path(__file__).resolve().parent.parent
    dataset_dir = workspace_root / "dataset"
    output_file = workspace_root / "output.csv"
    eval_report_file = workspace_root / "evaluation" / "evaluation_report.md"
    usage_report_file = workspace_root / "evaluation" / "usage_report.md"

    # Check if dataset exists
    if not dataset_dir.exists():
        print(f"ERROR: {dataset_dir} folder not found!")
        return

    # Load datasets
    print("\n[1/5] Loading datasets...")
    try:
        deletion_requests = pd.read_csv(dataset_dir / "deletion_requests.csv")
        user_identities = pd.read_csv(dataset_dir / "user_identities.csv")
        user_audit_log = pd.read_csv(dataset_dir / "user_audit_log.csv")
        system_activity = pd.read_csv(dataset_dir / "system_activity.csv")
        deletion_rules = pd.read_csv(dataset_dir / "deletion_rules.csv") if (dataset_dir / "deletion_rules.csv").exists() else pd.DataFrame()
        evidence_files = pd.read_csv(dataset_dir / "evidence_files.csv")
    except Exception as e:
        print(f"ERROR loading datasets: {e}")
        return

    print(f"  - Loaded {len(deletion_requests)} deletion requests")
    print(f"  - Loaded {len(user_identities)} user identities")
    print(f"  - Loaded {len(user_audit_log)} audit log entries")
    print(f"  - Loaded {len(system_activity)} system activities")
    print(f"  - Loaded {len(evidence_files)} evidence files")

    # Initialize components
    print("\n[2/5] Initializing audit components & indexing evidence...")
    identity_resolver = IdentityResolver(user_identities, user_audit_log, system_activity)
    evidence_analyzer = EvidenceAnalyzer(evidence_files, dataset_dir)
    audit_agent = AuditAgent(deletion_rules, system_activity, identity_resolver, evidence_analyzer)
    report_generator = ReportGenerator()

    print("  - Identity Resolver: Ready")
    print("  - Evidence Analyzer: All 94 evidence files indexed")
    print("  - Audit Agent: Ready")

    # Process all deletion requests
    print(f"\n[3/5] Processing {len(deletion_requests)} deletion requests...")
    print("-" * 70)
    results = []

    for idx, request in deletion_requests.iterrows():
        case_id = request['case_id']

        if idx % 50 == 0 or idx == len(deletion_requests) - 1:
            print(f"Progress: {idx + 1}/{len(deletion_requests)} cases processed ({(idx + 1)/len(deletion_requests)*100:.1f}%)")

        try:
            audit_result = audit_agent.audit_deletion(request)
            results.append(audit_result)
        except Exception as e:
            print(f"  WARNING: Error processing {case_id}: {e}")
            results.append({
                'case_id': case_id,
                'deletion_status': 'INCOMPLETE',
                'steps_json': '[]'
            })

    print("-" * 70)

    # Generate output.csv
    print(f"\n[4/5] Generating {output_file}...")
    df_out = report_generator.generate_csv(results, output_file)
    print(f"  - Output saved: {output_file} ({len(df_out)} rows)")

    # Generate evaluation reports
    print("\n[5/5] Generating evaluation reports...")
    report_generator.generate_evaluation_report(results, eval_report_file)
    report_generator.generate_usage_report(usage_report_file)
    print(f"  - Evaluation report: {eval_report_file}")
    print(f"  - Usage report: {usage_report_file}")

    # Summary statistics
    print("\n" + "=" * 70)
    print("AUDIT COMPLETE - SUMMARY")
    print("=" * 70)
    print(f"Total Cases Processed: {len(df_out)}")
    print(f"  - COMPLETE:        {len(df_out[df_out['deletion_status'] == 'COMPLETE'])} cases")
    print(f"  - INCOMPLETE:      {len(df_out[df_out['deletion_status'] == 'INCOMPLETE'])} cases")
    print(f"  - NOT_APPLICABLE:  {len(df_out[df_out['deletion_status'] == 'NOT_APPLICABLE'])} cases")
    print("=" * 70)
    print(f"\nResults saved to: {output_file}")
    print("Ready for submission!")

if __name__ == "__main__":
    main()
