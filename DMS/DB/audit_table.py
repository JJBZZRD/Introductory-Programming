from .config import conn, cursor

class AuditTable:  # Camp class has attributes matching columns in table
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
    def init_from_tuple(cls, camp_tuple):
        return cls(*camp_tuple)

    def display_info(self):
        return [str(self.auditID), str(self.table_name), str(self.recordID), str(self.field_name), str(self.old_value), str(self.new_value), str(self.action), str(self.created_time), str(self.changed_by)]

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
    def get_audit_logs():
        q = f"""
            SELECT * FROM audit_table WHERE changed_by IS NOT NULL
            """
        cursor.execute(q)
        return cursor.fetchall()