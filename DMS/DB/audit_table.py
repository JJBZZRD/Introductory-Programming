from .config import conn, cursor

class Camp:  # Camp class has attributes matching columns in table
    def __init__(self, auditID, table_name, recordID, field_name, old_value, new_value, action, created_time, changed_by):
        self.auditID = auditID
        self.table_name = table_name
        self.recordID = recordID
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.created_time = created_time

    @classmethod
    def init_from_tuple(cls, camp_tuple):
        return cls(*camp_tuple)

    def display_info(self):
        return [str(self.campID), str(self.location), str(self.shelter), str(self.water), str(self.food), str(self.medical_supplies), str(self.planID), self.created_time]
