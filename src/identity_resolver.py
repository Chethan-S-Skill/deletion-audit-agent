"""
Identity Resolver - Links all identities of a user across time
"""
import pandas as pd
from datetime import datetime

class IdentityResolver:
    def __init__(self, user_identities_df, user_audit_log_df):
        self.user_identities = user_identities_df
        self.user_audit_log = user_audit_log_df

    def get_user_id_from_email(self, email):
        """Get user_id from email address"""
        user = self.user_identities[self.user_identities['email'] == email]
        if not user.empty:
            return user.iloc[0]['user_id']

        # Check historical email changes in audit log
        audit_entries = self.user_audit_log[
            (self.user_audit_log['field_name'] == 'email') &
            ((self.user_audit_log['old_value'] == email) | (self.user_audit_log['new_value'] == email))
        ]
        if not audit_entries.empty:
            return audit_entries.iloc[0]['user_id']

        return None

    def resolve_all_identities(self, user_id, audit_timestamp):
        """
        Find all identities (emails, usernames, phone) for a user at a given timestamp.
        Includes current and historical identities.
        """
        all_identities = {
            'user_ids': set([user_id]),
            'emails': set(),
            'usernames': set(),
            'phones': set(),
            'full_names': set()
        }

        # Get current identities
        current = self.user_identities[self.user_identities['user_id'] == user_id]
        for _, row in current.iterrows():
            if pd.notna(row.get('email')):
                all_identities['emails'].add(row['email'])
            if pd.notna(row.get('username')):
                all_identities['usernames'].add(row['username'])
            if pd.notna(row.get('phone')):
                all_identities['phones'].add(row['phone'])
            if pd.notna(row.get('full_name')):
                all_identities['full_names'].add(row['full_name'])

        # Get historical identities from audit log
        audit_entries = self.user_audit_log[self.user_audit_log['user_id'] == user_id]

        # Filter by timestamp if provided
        if audit_timestamp:
            audit_entries = audit_entries[
                pd.to_datetime(audit_entries['event_time'], utc=True) <= pd.to_datetime(audit_timestamp, utc=True)
            ]

        for _, row in audit_entries.iterrows():
            field = row.get('field_name')
            old_value = row.get('old_value')
            new_value = row.get('new_value')

            if field == 'email':
                if pd.notna(old_value):
                    all_identities['emails'].add(old_value)
                if pd.notna(new_value):
                    all_identities['emails'].add(new_value)
            elif field == 'username':
                if pd.notna(old_value):
                    all_identities['usernames'].add(old_value)
                if pd.notna(new_value):
                    all_identities['usernames'].add(new_value)
            elif field == 'phone':
                if pd.notna(old_value):
                    all_identities['phones'].add(old_value)
                if pd.notna(new_value):
                    all_identities['phones'].add(new_value)
            elif field == 'full_name':
                if pd.notna(old_value):
                    all_identities['full_names'].add(old_value)
                if pd.notna(new_value):
                    all_identities['full_names'].add(new_value)

        return all_identities

    def user_exists(self, user_id):
        """Check if user ever existed in the system"""
        exists_in_current = user_id in self.user_identities['user_id'].values
        exists_in_history = user_id in self.user_audit_log['user_id'].values
        return exists_in_current or exists_in_history

    def get_merged_user_ids(self, user_id):
        """Find if this user was merged with other users"""
        merged_ids = set([user_id])

        # Check audit log for merge operations
        merge_entries = self.user_audit_log[
            (self.user_audit_log['user_id'] == user_id) &
            (self.user_audit_log['operation'] == 'MERGE')
        ]

        for _, row in merge_entries.iterrows():
            if pd.notna(row.get('merged_into')):
                merged_ids.add(row['merged_into'])
            if pd.notna(row.get('merged_from')):
                merged_ids.add(row['merged_from'])

        return merged_ids
