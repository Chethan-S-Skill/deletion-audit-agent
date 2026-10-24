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
        Returns list of evidence_ids that contain user data
        """
        matching_evidence = []

        # Get all identity strings to search for
        search_terms = set()
        search_terms.update(identities.get('emails', []))
        search_terms.update(identities.get('usernames', []))
        search_terms.update(identities.get('phones', []))
        search_terms.update(identities.get('full_names', []))
        search_terms.update([str(uid) for uid in identities.get('user_ids', [])])

        # Search through evidence files metadata
        for _, evidence in self.evidence_files.iterrows():
            evidence_id = evidence['file_id']
            file_path = self.evidence_dir / evidence.get('file_path', '')
            # Infer file type from path
            file_type = str(file_path).split('.')[-1] if '.' in str(file_path) else 'unknown'

            # Check metadata fields
            metadata_fields = ['description', 'tags', 'content_preview']
            for field in metadata_fields:
                if pd.notna(evidence.get(field)):
                    content = str(evidence[field]).lower()
                    for term in search_terms:
                        if term and str(term).lower() in content:
                            matching_evidence.append({
                                'evidence_id': evidence_id,
                                'file_path': str(file_path),
                                'file_type': file_type,
                                'matched_term': term,
                                'field': field
                            })
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
