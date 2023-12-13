from ..DB.audit_table import AuditTable
from .. import util

class AuditDataRetrieve:

    @staticmethod
    def get_audit_logs():
        return util.parse_result('AuditTable', AuditTable.get_audit_logs())