"""
Interactive Demo - Test the Deletion Audit Agent
Run this to see the agent analyze individual cases with full details
"""
import pandas as pd
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from identity_resolver import IdentityResolver
from evidence_analyzer import EvidenceAnalyzer
from audit_agent import AuditAgent

def print_separator(char='=', length=70):
    print(char * length)

def print_header(text):
    print_separator()
    print(f"  {text}")
    print_separator()

def print_section(title):
    print(f"\n[{title}]")
    print('-' * 70)

def main():
    print_header("DELETION AUDIT AGENT - Interactive Demo")

    # Load datasets
    print("\nLoading datasets...")
    deletion_requests = pd.read_csv('dataset/deletion_requests.csv')
    user_identities = pd.read_csv('dataset/user_identities.csv')
    user_audit_log = pd.read_csv('dataset/user_audit_log.csv')
    system_activity = pd.read_csv('dataset/system_activity.csv')
    evidence_files = pd.read_csv('dataset/evidence_files.csv')

    print(f"  # Loaded {len(deletion_requests)} deletion requests")
    print(f"  # Loaded {len(user_identities)} user identities")
    print(f"  # Loaded {len(user_audit_log)} audit log entries")
    print(f"  # Loaded {len(system_activity)} system activities")
    print(f"  # Loaded {len(evidence_files)} evidence files")

    # Initialize components
    print("\nInitializing audit components...")
    identity_resolver = IdentityResolver(user_identities, user_audit_log)
    evidence_analyzer = EvidenceAnalyzer(evidence_files, 'dataset/evidence')
    audit_agent = AuditAgent(identity_resolver, evidence_analyzer, system_activity)
    print("  # All components ready!")

    # Interactive loop
    while True:
        print_separator('=')
        print("\nOptions:")
        print("  1. Test specific case by case_id (e.g., case_01)")
        print("  2. Test specific case by number (1-518)")
        print("  3. Test random case")
        print("  4. Show available case IDs")
        print("  5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == '5':
            print("\nExiting demo. Goodbye!")
            break

        elif choice == '4':
            print_section("Available Case IDs (showing first 20)")
            for i, case_id in enumerate(deletion_requests['case_id'].head(20), 1):
                print(f"  {i:3d}. {case_id}")
            print(f"\n  ... and {len(deletion_requests) - 20} more cases")
            continue

        elif choice == '3':
            # Random case
            case = deletion_requests.sample(1).iloc[0]

        elif choice == '2':
            # By number
            try:
                num = int(input("Enter case number (1-518): ").strip())
                if num < 1 or num > len(deletion_requests):
                    print(f"ERROR: Please enter a number between 1 and {len(deletion_requests)}")
                    continue
                case = deletion_requests.iloc[num - 1]
            except ValueError:
                print("ERROR: Please enter a valid number")
                continue

        elif choice == '1':
            # By case_id
            case_id = input("Enter case_id (e.g., case_01): ").strip()
            matches = deletion_requests[deletion_requests['case_id'] == case_id]
            if len(matches) == 0:
                print(f"ERROR: Case '{case_id}' not found")
                continue
            case = matches.iloc[0]

        else:
            print("ERROR: Invalid choice")
            continue

        # Process the case
        print_header(f"Analyzing Case: {case['case_id']}")

        print_section("REQUEST DETAILS")
        print(f"  Case ID:          {case['case_id']}")
        print(f"  Email:            {case['email']}")
        print(f"  Requested At:     {case['requested_at']}")
        print(f"  Audit Timestamp:  {case['audit_at']}")
        print(f"  Reported Status:  {case['reported_status']}")
        print(f"  Request Text:     {case['request_text'][:80]}...")

        # Run audit
        print_section("RUNNING AUDIT ANALYSIS")
        print("  Phase 1: Identity Resolution...")
        print("  Phase 2: Evidence Discovery...")
        print("  Phase 3: System Activity Analysis...")
        print("  Phase 4: Risk Assessment...")
        print("  Phase 5: Compliance Verification...")
        print("  Phase 6: Decision & Remediation...")

        result = audit_agent.audit_deletion(case)

        print_section("AUDIT RESULT")
        print(f"  Final Status: {result['deletion_status']}")

        steps = json.loads(result['steps_json'])
        print(f"  Total Steps:  {len(steps)}")

        # Count phases
        phases = {}
        for step in steps:
            phase = step.get('phase', 'UNKNOWN')
            phases[phase] = phases.get(phase, 0) + 1

        print(f"\n  Phase Breakdown:")
        for phase, count in sorted(phases.items()):
            print(f"    - {phase}: {count} steps")

        # Show first 5 steps in detail
        print_section("REMEDIATION STEPS (First 5)")
        for i, step in enumerate(steps[:5], 1):
            print(f"\n  Step {step['step_no']}:")
            print(f"    Phase:       {step['phase']}")
            print(f"    System:      {step['system_id']}")
            print(f"    Resource:    {step['resource_id']}")
            print(f"    Operation:   {step['operation']}")
            print(f"    State:       {step['state']}")
            print(f"    Evidence:    {step['evidence_id']}")

        if len(steps) > 5:
            print(f"\n  ... and {len(steps) - 5} more steps")

        # Show full JSON option
        print_section("OPTIONS")
        show_full = input("  Show full JSON output? (y/n): ").strip().lower()

        if show_full == 'y':
            print_section("FULL JSON OUTPUT")
            print(json.dumps(json.loads(result['steps_json']), indent=2))

        print("\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
