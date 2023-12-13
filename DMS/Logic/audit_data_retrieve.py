from ..DB.audit_table import AuditTable
from .. import util

class AuditDataRetrieve:

    @staticmethod
    def get_all_audit_logs():
        return util.parse_result('AuditTable', AuditTable.get_all_audit_logs())
    
    @staticmethod
    def get_audit_logs(auditID=None, table_name=None, recordID=None, field_name=None, old_value=None, new_value=None, action=None, created_time=None, changed_by=None):
        audit_tuples = AuditTable.get_audit_logs(auditID=auditID, table_name=table_name, recordID=recordID, field_name=field_name, old_value=old_value, new_value=new_value, action=action, created_time=created_time, changed_by=changed_by)
        return util.parse_result('AuditTable', audit_tuples)