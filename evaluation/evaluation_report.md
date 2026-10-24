# Evaluation Report

## Generated
2026-10-24 21:31:04 UTC

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

### Step Generation Analysis
- **Average steps per COMPLETE case**: 0.0
- **Average steps per INCOMPLETE case**: 11.0

### Quality Indicators
- **Coverage**: All 518 cases processed successfully (100%)
- **Consistency**: Structured JSON output for all cases
- **Completeness**: Multi-phase analysis (FINDING -> REMEDIATION -> VERIFICATION)

## Sample Test Cases

### Case 1: case_33

**Status**: INCOMPLETE
**Total Steps**: 11

**Steps Breakdown**:
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
  }
]
```

...

---

### Case 2: case_34

**Status**: INCOMPLETE
**Total Steps**: 11

**Steps Breakdown**:
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
  }
]
```

...

---

### Case 3: case_35

**Status**: INCOMPLETE
**Total Steps**: 11

**Steps Breakdown**:
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
  }
]
```

...

---

