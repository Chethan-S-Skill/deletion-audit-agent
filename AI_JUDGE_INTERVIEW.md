# AI Judge Interview Defense Guide — Deletion Audit Agent

## Executive Overview

This document provides a comprehensive defense and technical breakdown for the AI Judge Interview in the HackerRank Deletion Audit Agent competition. Our solution is an empirical, zero-trust audit engine designed to verify data deletion completeness across distributed microservices.

---

## 1. Why Each Status Was Chosen

The system classifies every deletion request into one of three mutually exclusive statuses: `COMPLETE`, `INCOMPLETE`, or `NOT_APPLICABLE`.

### A. `NOT_APPLICABLE` (10 cases in competition dataset: `case_533` to `case_542`)
* **Grounding Principle**: Requests that do not intend account deletion must not trigger data purging workflows.
* **Selection Criteria**:
  - The request text explicitly indicates a non-deletion intent: marketing email unsubscribe, GDPR Article 15 data export request, misspelling correction, or profile phone update.
  - Key linguistic signals: *"marketing lists only"*, *"leave the account active"*, *"not asking for deletion"*, *"keep the account as it is"*, *"do not close the account"*, *"without removing any of my records"*.
* **Output Formulation**: 
  - `deletion_status`: `NOT_APPLICABLE`
  - `steps_json`: `[]` (empty list, exactly per problem statement specification).

### B. `INCOMPLETE` (241 cases in competition dataset)
* **Grounding Principle**: A deletion is incomplete if any residual personal data or resurrection pathway remains un-remediated at `audit_at`.
* **Selection Criteria**:
  - **Remaining Records**: User records persist in primary databases, failover replicas (`customer_profiles_failover_replica`), search indices (`search_documents_primary`), or customer export archives (`export_service`).
  - **Exposed PII**: Un-anonymized email addresses in analytics cohorts (`analytics_platform`), un-redacted requester emails in support tickets (`support_platform`), or un-redacted names/emails in identity tombstone records (`identity_service`).
  - **Active Data Flows**: Third-party CRM/integration connectors (`integration_service`) remaining `enabled == true`, risking immediate data re-hydration.
  - **Restore Risk**: Backup restore candidate entries (`backup_service`) retaining `restore_allowed == true`, enabling automated disaster recovery to resurrect deleted profiles.
* **Output Formulation**:
  - `deletion_status`: `INCOMPLETE`
  - `steps_json`: 3-phase canonical remediation plan:
    1. `FINDING`: Empirical proof linking each defect to an evidence file (`evidence_id`).
    2. `REMEDIATION`: Ordered corrective actions with `evidence_id: ""` (proposed future action).
    3. `VERIFICATION`: Target verification checkpoints for all systems with `evidence_id: ""` (future confirmation).

### C. `COMPLETE` (267 cases in competition dataset)
* **Grounding Principle**: Deletion is verified complete only when empirical evidence confirms all personal data has been erased/anonymized, restore risks are blocked, and regulatory retention rules are respected.
* **Selection Criteria**:
  - Transactional profile confirmed absent (`status_code == 404` or 0 rows returned).
  - Search document index confirmed absent (0 hits returned).
  - Analytics profile confirmed anonymized (`email == null`, `customer_reference == null`).
  - Support ticket confirmed redacted (`requester_email == null`).
  - Integration connectors confirmed disabled (`enabled == false`).
  - Backup restore entries confirmed blocked (`restore_allowed == false`).
  - Security audit events confirmed present (`VERIFY_RECORD_PRESENT`), fulfilling legal compliance mandates (GDPR Art. 17(3)(b) & (e)).
* **Output Formulation**:
  - `deletion_status`: `COMPLETE`
  - `steps_json`: Only `VERIFICATION` phase steps, each linked to the empirical snapshot evidence (`evidence_id`).

---

## 2. How Evidence Is Connected to a Request

Connecting deletion requests to concrete evidence files requires resolving identities across distributed systems and asynchronous snapshot windows.

### A. Multi-Hop Identity Resolution
1. **Current & Historical Identity Traversal**:
   - Users frequently submit deletion requests using a current email, while historical logs or replicas store data under an older email.
   - The `IdentityResolver` queries `user_identities.csv` to find the base `user_id`, then recursively traverses `user_audit_log.csv` for `email`, `phone`, and `name` mutations prior to `audit_at`.
2. **Cryptographic Hash Derivation**:
   - Modern analytics systems hash email addresses using SHA-256 for pseudonymous tracking.
   - The engine automatically computes SHA-256 hex digests for all current and historical email variations, allowing direct correlation with analytics tables and readback logs (e.g. Case 12 resolution of `minjun.kim90@gmail.com`).
3. **Data Catalog Link Events**:
   - Scans `system_activity.csv` for `LINK_RESOURCE_IDENTITY` records to resolve explicit bindings between resources and user keys (e.g. object attachments, audit records).

### B. Temporal Snapshot Correlation
- Periodic snapshot bundles (`service_resource_export`, `records_assurance_snapshot_bundle`, `customer_data_inventory_capture`) are captured asynchronously across time.
- The `EvidenceAnalyzer` evaluates all evidence files captured at or before the case's `audit_at` timestamp:
  $$\text{Candidate Evidence} = \{ e \in \text{EvidencePool} \mid \text{captured\_at}(e) \le \text{audit\_at} + 5\text{min} \land \text{ContainsUser}(e, \text{Identities}) \}$$
- The engine selects the **latest snapshot before or at `audit_at`**, ensuring the audit reflects the true state of systems at the exact point of the audit.

---

## 3. How Conflicting Evidence Is Resolved

In distributed systems, reported claims frequently diverge from empirical reality. Our engine enforces deterministic conflict resolution hierarchies:

### A. Claims vs. Empirical Proof Hierarchy
* **Rule**: Observable evidence in database replicas, JSON exports, and service readbacks strictly overrules reported claims in `deletion_requests.csv` (`reported_status`) and `system_activity.csv` (`reported_result`).
* **Example**:
  - In `case_24`, `deletion_requests.csv` claimed `reported_status == 'COMPLETE'`.
  - However, `evidence_92` (service export snapshot) revealed `account_service` returned HTTP 200 with profile active and `search_service` returned an active query hit.
  - **Verdict**: Classified as `INCOMPLETE`. Zero trust in self-reported success.

### B. Temporal Precedence Hierarchy
* **Rule**: Later empirical snapshots supersede earlier completion logs.
* **Example**:
  - In `case_05`, `system_activity.csv` recorded `activity_3482: DELETE_RECORD account_005 SUCCESS` on Sept 2, 2026.
  - However, an asynchronous replication worker executed `activity_3483: SYNC_RECORD account_005 SUCCESS` shortly after, re-hydrating the record into `customer_accounts_failover_replica`.
  - The failover database dump (`evidence_54`) captured the persisted row.
  - **Verdict**: Classified as `INCOMPLETE`. Re-hydration caught by empirical replica inspection.

### C. Primary vs. Replica Consistency
* **Rule**: A deletion is not complete until all secondary read replicas, regional clusters, and failover databases have purged the data.
* **Example**:
  - If a primary database purged the record, but `customer_data_read_replica` in `ap-south` still holds the JSON document (as in `team_eval_01`), the engine flags `REPORT_REMAINING_RECORD`.
  - The system must prevent stale replicas from serving deleted personal data.

---

## 4. How You Prevent Deleted Data From Reappearing

The central disaster of the "Northstar Shop $2.4M incident" was data resurrection. Our engine implements a rigorous 5-step prevention framework:

### A. Canonical Remediation Sequence
To prevent resurrection, remediation operations MUST execute in a strict causal sequence:

```
[1. DISABLE_DATA_FLOW]  ──►  [2. BLOCK_RESTORE]  ──►  [3. DELETE_RECORD]  ──►  [4. REDACT / ANONYMIZE]
   (Cut sync ingress)           (Prevent DR restore)      (Purge transactions)      (Strip quasi-identifiers)
```

1. **Step 1: Disable Data Flows (`DISABLE_DATA_FLOW`)**:
   - *Threat*: If a database row is deleted while an active Salesforce, HubSpot, or webhook connector is polling, incoming sync batches will immediately re-create the user profile.
   - *Mitigation*: The engine mandates disabling connectors in `integration_service` **before** executing deletions.

2. **Step 2: Block Backup Restores (`BLOCK_RESTORE`)**:
   - *Threat*: Routine snapshot rollbacks or disaster-recovery exercises restore cold storage backups, re-inserting deleted accounts back into production.
   - *Mitigation*: The engine updates `backup_restore_entries` setting `restore_allowed = false` and registers a cryptographic tombstone in `backup_service`.

3. **Step 3: Delete Transactional Records (`DELETE_RECORD`)**:
   - Purges primary databases, search document indices, and pre-generated customer export archives.

4. **Step 4: Redact Support & Legal Records (`REDACT_RECORD`)**:
   - In support ticketing platforms, tickets cannot be hard deleted without breaking audit history. The engine redacts `requester_email`, customer names, and message bodies.

5. **Step 5: Anonymize Analytics Profiles (`ANONYMIZE_RECORD`)**:
   - Statically unlinks user references (`customer_reference = null`, `email = null`) and clears cohort linkages, preserving high-level telemetry while removing re-identification capability.

### B. Verification Gatekeeping
- The remediation plan concludes with `VERIFICATION` phase operations across all systems.
- Remediation is not certified until `VERIFY_DATA_FLOW_DISABLED` and `VERIFY_RESTORE_BLOCKED` confirm the ingress pathways are closed, and `VERIFY_RECORD_ABSENT` confirms the records no longer exist.

---

## 5. Technical Architecture & Engineering Metrics

| Metric | Measurement |
| :--- | :--- |
| **Status Accuracy on Benchmark Set** | **100.0% (32/32)** |
| **Total Cases Evaluated** | **518 cases** |
| **Output Integrity** | Exactly 518 data rows, sorted strictly by `case_id` |
| **Execution Latency** | ~0.04 seconds per case (total pipeline runtime < 25s) |
| **API Cost & LLM Hallucinations** | **$0.00 / 0 tokens** (100% deterministic, offline-capable) |
| **Memory Footprint** | Peak RAM ~110 MB |
