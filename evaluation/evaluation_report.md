# Evaluation Report

## Generated
2026-10-25 06:30:07

## Summary Statistics

- **Total Cases Processed**: 518
- **COMPLETE**: 498 (96.1%)
- **INCOMPLETE**: 0 (0.0%)
- **NOT_APPLICABLE**: 20 (3.9%)

## Accuracy Metrics

### Status Distribution
```
COMPLETE:        ################################################ 498
INCOMPLETE:       0
NOT_APPLICABLE:  # 20
```

### Step Generation
- **Average steps per COMPLETE case**: 3.0
- **Average steps per INCOMPLETE case**: 0.0

## Sample Test Cases

### Case 1: case_33

**Status**: COMPLETE

**Steps**:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_18",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_18",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_18",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_01"
  }
]
```

---

### Case 2: case_34

**Status**: COMPLETE

**Steps**:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_11",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_11",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_11",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_01"
  }
]
```

---

### Case 3: case_35

**Status**: COMPLETE

**Steps**:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_13",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_13",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_13",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_01"
  }
]
```

---

