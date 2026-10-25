"""
Identity Resolver - Comprehensive multi-hop identity resolution across time
Links user identities, historical audit logs, SHA-256 hashes, and data catalog link events.
"""
import re
import hashlib
import pandas as pd

class IdentityResolver:
    def __init__(self, user_identities_df, user_audit_log_df, system_activity_df=None):
        self.user_identities = user_identities_df
        self.user_audit_log = user_audit_log_df
        self.system_activity = system_activity_df

    def get_user_id_from_email(self, email):
        """Get user_id from email address with case-insensitive and historical matching"""
        if not email or pd.isna(email):
            return None
        em_lower = email.strip().lower()
        
        # Match current identities
        user = self.user_identities[self.user_identities['email'].astype(str).str.lower() == em_lower]
        if not user.empty:
            return user.iloc[0]['user_id']

        # Match historical email changes in audit log
        audit_entries = self.user_audit_log[
            (self.user_audit_log['field_name'] == 'email') &
            ((self.user_audit_log['old_value'].astype(str).str.lower() == em_lower) | 
             (self.user_audit_log['new_value'].astype(str).str.lower() == em_lower))
        ]
        if not audit_entries.empty:
            return audit_entries.iloc[0]['user_id']

        return None

    def resolve_all_identities(self, email, user_id=None, audit_timestamp=None):
        """
        Find all identities (emails, usernames, phones, names, hashes, user_ids) for a user.
        Includes current identities, historical audit updates, computed SHA-256 hashes,
        and system activity identity links.
        """
        em_clean = email.strip().lower() if email and pd.notna(email) else None
        if not user_id and em_clean:
            user_id = self.get_user_id_from_email(em_clean)

        emails = {em_clean} if em_clean else set()
        user_ids = {user_id} if user_id else set()
        phones = set()
        names = set()
        hashes = set()

        if user_id:
            # Current identities
            u_rows = self.user_identities[self.user_identities['user_id'] == user_id]
            for _, r in u_rows.iterrows():
                if pd.notna(r.get('email')):
                    emails.add(str(r['email']).strip().lower())
                if pd.notna(r.get('phone')):
                    phones.add(str(r['phone']).strip())
                if pd.notna(r.get('name')):
                    names.add(str(r['name']).strip().lower())
                elif pd.notna(r.get('full_name')):
                    names.add(str(r['full_name']).strip().lower())
                if pd.notna(r.get('email_hash')):
                    hashes.add(str(r['email_hash']).strip().lower())

            # Historical audit log entries
            a_rows = self.user_audit_log[self.user_audit_log['user_id'] == user_id]
            if audit_timestamp:
                try:
                    cutoff = pd.to_datetime(audit_timestamp, utc=True)
                    a_rows = a_rows[pd.to_datetime(a_rows['event_time'], utc=True) <= cutoff]
                except Exception:
                    pass

            for _, r in a_rows.iterrows():
                fn = r.get('field_name')
                old_val = r.get('old_value')
                new_val = r.get('new_value')

                if fn == 'email':
                    if pd.notna(old_val): emails.add(str(old_val).strip().lower())
                    if pd.notna(new_val): emails.add(str(new_val).strip().lower())
                elif fn == 'phone':
                    if pd.notna(old_val): phones.add(str(old_val).strip())
                    if pd.notna(new_val): phones.add(str(new_val).strip())
                elif fn in ['name', 'full_name']:
                    if pd.notna(old_val): names.add(str(old_val).strip().lower())
                    if pd.notna(new_val): names.add(str(new_val).strip().lower())

        # Check system activity for LINK_RESOURCE_IDENTITY events
        if self.system_activity is not None and not self.system_activity.empty:
            link_events = self.system_activity[self.system_activity['event_type'] == 'LINK_RESOURCE_IDENTITY']
            for _, r in link_events.iterrows():
                det = str(r['details']).lower()
                if any(e in det for e in emails) or (user_id and user_id.lower() in det):
                    for u in re.findall(r'user_\d+', det):
                        user_ids.add(u)
                    for e in re.findall(r'[\w\.-]+@[\w\.-]+', det):
                        emails.add(e.lower())

        # Compute SHA-256 hashes for all current and historical emails
        for em in list(emails):
            h = hashlib.sha256(em.encode('utf-8')).hexdigest().lower()
            hashes.add(h)

        # Build full unified key set for lookup
        all_keys = set()
        for e in emails: all_keys.add(e)
        for u in user_ids: all_keys.add(u)
        for h in hashes: all_keys.add(h)
        for p in phones: all_keys.add(p)

        return {
            'user_id': user_id,
            'user_ids': user_ids,
            'emails': emails,
            'phones': phones,
            'names': names,
            'hashes': hashes,
            'all_keys': all_keys
        }

    def user_exists(self, email=None, user_id=None):
        """Check if user exists in the system records"""
        if user_id:
            in_curr = user_id in self.user_identities['user_id'].values
            in_hist = user_id in self.user_audit_log['user_id'].values
            return in_curr or in_hist
        if email:
            uid = self.get_user_id_from_email(email)
            return uid is not None
        return False
