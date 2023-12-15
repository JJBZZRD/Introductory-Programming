from .config import conn, cursor


class AuditTable:  # AuditTable class has attributes matching columns in table
    def __init__(self, auditID, table_name, recordID, field_name, old_value, new_value, action, created_time, changed_by):
        self.auditID = auditID
        self.table_name = table_name
        self.recordID = recordID
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.action = action
        self.created_time = created_time
        self.changed_by = changed_by

    @classmethod
    def init_from_tuple(cls, audit_tuple):
        return cls(*audit_tuple)

    def display_info(self):
        return [str(self.auditID), str(self.table_name), str(self.recordID), str(self.field_name), str(self.old_value),
                str(self.new_value), str(self.action), str(self.created_time), str(self.changed_by)]

    @staticmethod
    def log_user_login_history(username, time):
        q = f"""
            INSERT INTO current_user (username, time)
            VALUES ('{username}', '{time}')
            """
        cursor.execute(q)
        conn.commit()
        record_id = cursor.execute("SELECT last_insert_rowid() FROM current_user").fetchone()
        return True if record_id else False
    
    @staticmethod
    def get_all_audit_logs():
        q = f"""
            SELECT * FROM audit WHERE changed_by IS NOT NULL
            """
        cursor.execute(q)
        return cursor.fetchall()

    @staticmethod 
    def get_audit_logs(auditID=None, table_name=None, recordID=None, field_name=None, old_value=None, new_value=None, action=None, created_time=None, changed_by=None):

        q = """
            SELECT * FROM audit WHERE changed_by IS NOT NULL
            """

        if auditID:
            q += f" AND auditID = {auditID}"
        if table_name:
            q += f" AND table_name = '{table_name}'"
        if recordID:
            q += f" AND recordID = {recordID}"
        if field_name:
            q += f" AND field_name = '{field_name}'"
        if old_value:
            q += f" AND old_value = '{old_value}'"
        if new_value:
            q += f" AND new_value = '{new_value}'"
        if action:
            q += f" AND action = '{action}'"
        if created_time:
            q += f" AND created_time = '{created_time}'"
        if changed_by:
            q += f" AND changed_by = '{changed_by}'"

        cursor.execute(q)
        return cursor.fetchall()
