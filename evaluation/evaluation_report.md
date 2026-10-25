# Evaluation Report

## Generated
2026-10-24 23:23:37

## Summary Statistics

- **Total Cases Processed**: 518
- **COMPLETE**: 0 (0.0%)
- **INCOMPLETE**: 498 (96.1%)
- **NOT_APPLICABLE**: 20 (3.9%)

## Accuracy Metrics

### Status Distribution
```
COMPLETE:         0
INCOMPLETE:      ################################################ 498
NOT_APPLICABLE:  # 20
```

### Step Generation
- **Average steps per COMPLETE case**: 0.0
- **Average steps per INCOMPLETE case**: 11.0

## Sample Test Cases

### Case 1: case_33

**Status**: INCOMPLETE

**Steps**:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_18",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_18",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

---

### Case 2: case_34

**Status**: INCOMPLETE

**Steps**:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_11",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_11",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

---

### Case 3: case_35

**Status**: INCOMPLETE

**Steps**:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_13",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_13",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_8264",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_6344",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "deletion_worker",
    "resource_id": "backup_3382",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

---

