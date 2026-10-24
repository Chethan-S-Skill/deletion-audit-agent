"""
Quick test to verify the solution works before running on full dataset
"""
import sys
sys.path.insert(0, 'src')

import pandas as pd
from pathlib import Path

print("Testing solution components...")

# Load datasets
print("\n1. Loading datasets...")
dataset_dir = Path("dataset")
deletion_requests = pd.read_csv(dataset_dir / "deletion_requests.csv")
user_identities = pd.read_csv(dataset_dir / "user_identities.csv")
user_audit_log = pd.read_csv(dataset_dir / "user_audit_log.csv")
system_activity = pd.read_csv(dataset_dir / "system_activity.csv")
deletion_rules = pd.read_csv(dataset_dir / "deletion_rules.csv")
evidence_files = pd.read_csv(dataset_dir / "evidence_files.csv")

print(f"OK: Loaded {len(deletion_requests)} deletion requests")
print(f"OK: Loaded {len(user_identities)} user identities")
print(f"OK: Loaded {len(user_audit_log)} audit log entries")
print(f"OK: Loaded {len(system_activity)} system activities")
print(f"OK: Loaded {len(evidence_files)} evidence files")

# Initialize components
print("\n2. Initializing components...")
from identity_resolver import IdentityResolver
from evidence_analyzer import EvidenceAnalyzer
from audit_agent import AuditAgent

identity_resolver = IdentityResolver(user_identities, user_audit_log)
evidence_analyzer = EvidenceAnalyzer(evidence_files, dataset_dir / "evidence")
audit_agent = AuditAgent(deletion_rules, system_activity, identity_resolver, evidence_analyzer)

print("OK: All components initialized")

# Test with first case
print("\n3. Testing with first deletion request...")
test_case = deletion_requests.iloc[0]
print(f"   Case ID: {test_case['case_id']}")
print(f"   Email: {test_case['email']}")
print(f"   Audit timestamp: {test_case['audit_at']}")

result = audit_agent.audit_deletion(test_case)
print(f"\nOK: Test result:")
print(f"   Status: {result['deletion_status']}")
print(f"   Steps: {len(result['steps_json'])} characters")

print("\nSUCCESS: All tests passed! Ready to run on full dataset.")
print("\nTo run on full dataset:")
print("   python src/main.py")
