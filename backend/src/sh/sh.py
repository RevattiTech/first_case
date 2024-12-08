import re

from marshmallow import Schema, fields as f, validate, validates, ValidationError


URL_REGEX = r'^(https?:\/\/)?([a-zA-Z0-9.-]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$'


def validate_url(value):
    if not re.match(URL_REGEX, value):
        raise ValidationError("Invalid URL, IP, or domain format.")

    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', value):
        octets = value.split('.')
        for octet in octets:
            if not (0 <= int(octet) <= 255):
                raise ValidationError("IP address octets must be between 0 and 255.")

    return value

class ScanSh(Schema):
    url = f.Str(required=True, validate=validate_url)
    user_id = f.Integer(required=False)



