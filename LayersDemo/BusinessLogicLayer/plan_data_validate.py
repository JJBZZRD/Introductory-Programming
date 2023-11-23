from datetime import datetime


class ValidatePlan:

    @staticmethod
    def validate(value, message):
        if isinstance(value, str) and value:
            return value
        elif value is None or value == "":
            print("Please enter" + str(value))
            return None
        else:
            raise ValueError(message)

    @staticmethod
    def validate_name(name: str):
        return ValidatePlan.validate(name, "Invalid name")

    @staticmethod
    def validate_plan_type(plan_type: str):
        return ValidatePlan.validate(plan_type, "Invalid plan type")

    @staticmethod
    def validate_region(region: str):
        return ValidatePlan.validate(region, "Invalid region")

    @staticmethod
    def validate_event(event: str):
        return ValidatePlan.validate(event, "Invalid event")

    @staticmethod
    def validate_description(description: str):
        return ValidatePlan.validate(description, "Invalid description")

    @staticmethod
    def validate_date(start_time, end_time):
        try:
            if not all(isinstance(date, str) for date in [start_time, end_time]):
                raise TypeError("Invalid input type")

            if not start_time or not end_time:
                print("Please enter date")
                return None

            start_time = datetime.strptime(start_time, '%d/%m/%y')
            end_time = datetime.strptime(end_time, '%d/%m/%y')

            for date in [start_time, end_time]:
                if not 1 <= date.day <= 31:
                    raise ValueError("Invalid day")
                elif not 1 <= date.month <= 12:
                    raise ValueError("Invalid month")
                elif not 1 <= date.year <= 9999:
                    raise ValueError("Invalid year")

            if start_time > end_time:
                raise ValueError("Invalid. End time must be after start time")

            return start_time, end_time

        except ValueError:
            print("Invalid input")
            return None
