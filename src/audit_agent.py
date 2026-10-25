"""
Audit Agent - Core Privacy Compliance Decision Engine
Determines deletion status (COMPLETE, INCOMPLETE, NOT_APPLICABLE) based on verified empirical evidence
and constructs canonically-ordered remediation/verification plans per the problem specification.
"""
import json
import pandas as pd

FINDING_OPS = {
    'REPORT_REMAINING_RECORD': 1,
    'REPORT_EXPOSED_PII': 2,
    'REPORT_ACTIVE_DATA_FLOW': 3,
    'REPORT_RESTORE_RISK': 4
}
REMEDIATION_OPS = {
    'DISABLE_DATA_FLOW': 1,
    'BLOCK_RESTORE': 2,
    'DELETE_RECORD': 3,
    'REDACT_RECORD': 4,
    'ANONYMIZE_RECORD': 5
}
VERIFICATION_OPS = {
    'VERIFY_RECORD_ABSENT': 1,
    'VERIFY_RECORD_PRESENT': 2,
    'VERIFY_RECORD_REDACTED': 3,
    'VERIFY_RECORD_ANONYMIZED': 4,
    'VERIFY_DATA_FLOW_DISABLED': 5,
    'VERIFY_RESTORE_BLOCKED': 6
}
PHASE_RANKS = {'FINDING': 1, 'REMEDIATION': 2, 'VERIFICATION': 3}

NOT_APP_PHRASES = [
    'leave the account active',
    'not asking for deletion',
    'keep the account as it is',
    'do not close the account',
    'without removing any of my records',
    'marketing lists only',
    'not a request to erase',
    'leave my profile and purchase history in place',
    'continue using the service',
    "don't delete or change anything",
    'do not delete'
]

class AuditAgent:
    def __init__(self, deletion_rules_df, system_activity_df, identity_resolver, evidence_analyzer):
        self.deletion_rules = deletion_rules_df
        self.system_activity = system_activity_df
        self.identity_resolver = identity_resolver
        self.evidence_analyzer = evidence_analyzer

    def is_not_applicable(self, request_text):
        """Check if request is not an actual account deletion request (e.g. marketing opt-out, data export)"""
        t = str(request_text).lower()
        return any(p in t for p in NOT_APP_PHRASES)

    def sort_steps(self, steps):
        """Sort steps canonically by phase, operation rank, system_id, and resource_id"""
        def sort_key(s):
            p_rank = PHASE_RANKS.get(s['phase'], 99)
            op = s['operation']
            if s['phase'] == 'FINDING':
                op_rank = FINDING_OPS.get(op, 99)
            elif s['phase'] == 'REMEDIATION':
                op_rank = REMEDIATION_OPS.get(op, 99)
            else:
                op_rank = VERIFICATION_OPS.get(op, 99)
            return (p_rank, op_rank, s['system_id'], s['resource_id'])

        sorted_steps = sorted(steps, key=sort_key)
        for i, s in enumerate(sorted_steps, 1):
            s['step_no'] = i
        return sorted_steps

    def audit_deletion(self, deletion_request):
        """
        Audit a deletion request:
        1. Check for non-deletion intent (NOT_APPLICABLE)
        2. Resolve all user identities across time
        3. Match against latest empirical evidence snapshot at/before audit timestamp
        4. Detect findings vs verified states
        5. Generate sorted canonical steps
        """
        cid = deletion_request['case_id']
        email = deletion_request['email']
        req_text = deletion_request.get('request_text', '')
        audit_at_str = deletion_request['audit_at']
        audit_dt = pd.to_datetime(audit_at_str, utc=True)

        # 1. Check NOT_APPLICABLE
        if self.is_not_applicable(req_text):
            return {
                'case_id': cid,
                'deletion_status': 'NOT_APPLICABLE',
                'steps_json': '[]'
            }

        # 2. Multi-hop Identity Resolution
        u_info = self.identity_resolver.resolve_all_identities(email, audit_timestamp=audit_at_str)
        user_keys = {k.lower() for k in u_info['all_keys'] if k}

        # 3. Evidence Snapshot Retrieval
        selected_fid, obs_for_user = self.evidence_analyzer.find_observations_for_user(user_keys, audit_dt)

        # 4. Findings vs Verifications
        findings = []
        verifications = []

        for obs in obs_for_user:
            st = obs['state_type']
            sys_id = obs['system_id']
            rid = obs['resource_id']
            fid = obs['evidence_id']

            if st == 'REMAINING_RECORD':
                findings.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'finding_op': 'REPORT_REMAINING_RECORD',
                    'rem_op': 'DELETE_RECORD',
                    'ver_op': 'VERIFY_RECORD_ABSENT',
                    'state': 'PRESENT',
                    'rem_state': 'ABSENT',
                    'evidence_id': fid
                })
            elif st == 'EXPOSED_PII_ANALYTICS':
                findings.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'finding_op': 'REPORT_EXPOSED_PII',
                    'rem_op': 'ANONYMIZE_RECORD',
                    'ver_op': 'VERIFY_RECORD_ANONYMIZED',
                    'state': 'PRESENT',
                    'rem_state': 'ANONYMIZED',
                    'evidence_id': fid
                })
            elif st in ['EXPOSED_PII_SUPPORT', 'EXPOSED_PII_TOMBSTONE']:
                findings.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'finding_op': 'REPORT_EXPOSED_PII',
                    'rem_op': 'REDACT_RECORD',
                    'ver_op': 'VERIFY_RECORD_REDACTED',
                    'state': 'PRESENT',
                    'rem_state': 'REDACTED',
                    'evidence_id': fid
                })
            elif st == 'ACTIVE_DATA_FLOW':
                findings.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'finding_op': 'REPORT_ACTIVE_DATA_FLOW',
                    'rem_op': 'DISABLE_DATA_FLOW',
                    'ver_op': 'VERIFY_DATA_FLOW_DISABLED',
                    'state': 'ACTIVE',
                    'rem_state': 'DISABLED',
                    'evidence_id': fid
                })
            elif st == 'RESTORE_RISK':
                findings.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'finding_op': 'REPORT_RESTORE_RISK',
                    'rem_op': 'BLOCK_RESTORE',
                    'ver_op': 'VERIFY_RESTORE_BLOCKED',
                    'state': 'ACTIVE',
                    'rem_state': 'BLOCKED',
                    'evidence_id': fid
                })
            elif st == 'VERIFY_ABSENT':
                verifications.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'operation': 'VERIFY_RECORD_ABSENT',
                    'state': 'ABSENT',
                    'evidence_id': fid
                })
            elif st == 'VERIFY_PRESENT':
                verifications.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'operation': 'VERIFY_RECORD_PRESENT',
                    'state': 'PRESENT',
                    'evidence_id': fid
                })
            elif st == 'VERIFY_ANONYMIZED':
                verifications.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'operation': 'VERIFY_RECORD_ANONYMIZED',
                    'state': 'ANONYMIZED',
                    'evidence_id': fid
                })
            elif st in ['VERIFY_REDACTED', 'VERIFY_TOMBSTONE_REDACTED']:
                verifications.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'operation': 'VERIFY_RECORD_REDACTED',
                    'state': 'REDACTED',
                    'evidence_id': fid
                })
            elif st == 'VERIFY_DATA_FLOW_DISABLED':
                verifications.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'operation': 'VERIFY_DATA_FLOW_DISABLED',
                    'state': 'DISABLED',
                    'evidence_id': fid
                })
            elif st == 'VERIFY_RESTORE_BLOCKED':
                verifications.append({
                    'system_id': sys_id,
                    'resource_id': rid,
                    'operation': 'VERIFY_RESTORE_BLOCKED',
                    'state': 'BLOCKED',
                    'evidence_id': fid
                })

        is_incomplete = len(findings) > 0
        final_steps = []

        if is_incomplete:
            status = 'INCOMPLETE'
            # 1. FINDING phase steps (with evidence_id)
            for f in findings:
                final_steps.append({
                    'phase': 'FINDING',
                    'system_id': f['system_id'],
                    'resource_id': f['resource_id'],
                    'operation': f['finding_op'],
                    'state': f['state'],
                    'evidence_id': f['evidence_id']
                })
            # 2. REMEDIATION phase steps (proposed remediation, evidence_id = "")
            for f in findings:
                final_steps.append({
                    'phase': 'REMEDIATION',
                    'system_id': f['system_id'],
                    'resource_id': f['resource_id'],
                    'operation': f['rem_op'],
                    'state': f['rem_state'],
                    'evidence_id': ""
                })
            # 3. VERIFICATION phase steps (future verification plan, evidence_id = "")
            # Verified clean systems
            for v in verifications:
                final_steps.append({
                    'phase': 'VERIFICATION',
                    'system_id': v['system_id'],
                    'resource_id': v['resource_id'],
                    'operation': v['operation'],
                    'state': v['state'],
                    'evidence_id': ""
                })
            # Remediated systems
            for f in findings:
                final_steps.append({
                    'phase': 'VERIFICATION',
                    'system_id': f['system_id'],
                    'resource_id': f['resource_id'],
                    'operation': f['ver_op'],
                    'state': f['rem_state'],
                    'evidence_id': ""
                })
        else:
            status = 'COMPLETE'
            # Only VERIFICATION phase steps with evidence_id
            for v in verifications:
                final_steps.append({
                    'phase': 'VERIFICATION',
                    'system_id': v['system_id'],
                    'resource_id': v['resource_id'],
                    'operation': v['operation'],
                    'state': v['state'],
                    'evidence_id': v['evidence_id']
                })

        sorted_res = self.sort_steps(final_steps)
        return {
            'case_id': cid,
            'deletion_status': status,
            'steps_json': json.dumps(sorted_res)
        }
