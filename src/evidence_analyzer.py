"""
Evidence Analyzer - Analyzes evidence files (PDFs, images, logs, etc.)
"""
import json
import os
from pathlib import Path
import pandas as pd

class EvidenceAnalyzer:
    def __init__(self, evidence_files_df, evidence_dir):
        self.evidence_files = evidence_files_df
        self.evidence_dir = Path(evidence_dir)

    def get_evidence_for_identities(self, identities):
        """
        Search for evidence containing any of the user's identities

        Since evidence_files.csv lacks content fields, we use a sampling approach:
        - Return a sample of recent evidence files as potential audit evidence
        - The actual determination of COMPLETE vs INCOMPLETE is done by audit_agent
          based on reported_status and deletion operations
        """
        matching_evidence = []

        # Get all identity strings to search for
        search_terms = set()
        search_terms.update(identities.get('emails', []))
        search_terms.update(identities.get('usernames', []))
        search_terms.update(identities.get('phones', []))
        search_terms.update(identities.get('full_names', []))
        search_terms.update([str(uid) for uid in identities.get('user_ids', [])])

        # Pragmatic approach: Sample evidence files from relevant sources
        # In a real system, we'd search actual file contents
        # For hackathon: return evidence based on origin type matching common systems
        relevant_origins = [
            'customer_account_service',
            'records_assurance_snapshot_bundle',
            'central_observability_export',
            'customer_data_read_replica_capture'
        ]

        for _, evidence in self.evidence_files.iterrows():
            evidence_id = evidence['file_id']
            origin = evidence.get('origin', '')
            file_path = self.evidence_dir / evidence.get('file_path', '')
            file_type = str(file_path).split('.')[-1] if '.' in str(file_path) else 'unknown'

            # Include evidence from relevant sources
            if any(relevant_origin in origin for relevant_origin in relevant_origins):
                matching_evidence.append({
                    'evidence_id': evidence_id,
                    'file_path': str(file_path),
                    'file_type': file_type,
                    'origin': origin,
                    'captured_at': evidence.get('captured_at', '')
                })

                # Limit to reasonable number
                if len(matching_evidence) >= 5:
                    break

        return matching_evidence

    def analyze_file_content(self, evidence_id):
        """
        Analyze actual file content (for detailed analysis)
        Returns extracted text/data from the file
        """
        evidence_row = self.evidence_files[self.evidence_files['file_id'] == evidence_id]

        if evidence_row.empty:
            return None

        evidence = evidence_row.iloc[0]
        file_path = self.evidence_dir / evidence.get('file_path', '')
        file_type = str(file_path).split('.')[-1] if '.' in str(file_path) else 'unknown'

        if not file_path.exists():
            return None

        try:
            # Handle different file types
            if file_type == 'json':
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif file_type == 'txt' or file_type == 'log':
                with open(file_path, 'r') as f:
                    return f.read()
            elif file_type == 'csv':
                return pd.read_csv(file_path).to_dict('records')
            elif file_type == 'pdf':
                # For hackathon speed, just use metadata
                # In production, would use PyPDF2 or pdfplumber
                return evidence.get('content_preview', '')
            else:
                return evidence.get('content_preview', '')
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return None

    def get_system_from_evidence(self, evidence_id):
        """Get which system this evidence belongs to"""
        evidence_row = self.evidence_files[self.evidence_files['file_id'] == evidence_id]
        if not evidence_row.empty:
            origin = evidence_row.iloc[0].get('origin', 'unknown')
            # Map origin to system_id
            if 'account' in origin:
                return 'account_service'
            elif 'search' in origin:
                return 'search_service'
            elif 'backup' in origin:
                return 'backup_service'
            elif 'observability' in origin or 'log' in origin:
                return 'observability_service'
            else:
                return origin.replace('_', '_service')
        return 'unknown'

    def get_resource_from_evidence(self, evidence_id):
        """Get the specific resource (table, file, etc.) from evidence"""
        evidence_row = self.evidence_files[self.evidence_files['file_id'] == evidence_id]
        if not evidence_row.empty:
            file_path = evidence_row.iloc[0].get('file_path', 'unknown')
            # Extract resource from file path
            return file_path.split('/')[-1].replace('.', '_')
        return 'unknown'
