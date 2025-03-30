import re


class Valid:
    @staticmethod
    def String(value):
        return isinstance(value, str)

    @staticmethod
    def Boolean(value):
        return isinstance(value, bool)

    @staticmethod
    def Int(value):
        return isinstance(value, int)

    @staticmethod
    def Float(value):
        return isinstance(value, float)

    @staticmethod
    def GT(min_value):
        def validator(value):
            return value > min_value
        return validator

    @staticmethod
    def LT(max_value):
        def validator(value):
            return value < max_value
        return validator

    @staticmethod
    def Length(min_length, max_length):
        def validator(value):
            return min_length < len(value) < max_length
        return validator

    @staticmethod
    def LengthEquals(length):
        def validator(value):
            return len(value) == length
        return validator

    @staticmethod
    def PhoneNumber(value):
        phone_number_regex = r'^\+?1?\d{9,15}$'
        return re.match(phone_number_regex, value) is not None

    @staticmethod
    def Email(value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, value) is not None

    @staticmethod
    def NotEmpty(value):
        return bool(value)

    @staticmethod
    def IsDigit(value):
        return value.isdigit()

    @staticmethod
    def IsAlpha(value):
        return value.isalpha()

    @staticmethod
    def IsAlnum(value):
        return value.isalnum()

    @staticmethod
    def Date(value):
        date_regex = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(date_regex, value) is not None

    @staticmethod
    def File(value):
        return isinstance(value, (str, bytes)) and bool(value)

    @staticmethod
    def Equals(expected_value):
        def validator(value):
            return value == expected_value
        return validator


def validate(validations):
    errors = {}
    for field, (value, validators) in validations.items():
        for validator in validators:
            if not validator(value):
                errors[field] = f"Invalid value for {field}"
                break
    return errors