from marshmallow import Schema, fields, pre_load
from ...utils.utils import pre_load_date_date_fields


class Signature13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    NAME = fields.String(required=True)
    TITLE = fields.String(required=True)
    PHONE = fields.String()
    SIGNATURE = fields.String(required=True)
    CITY = fields.String(required=True)
    STATEORCOUNTRY = fields.String(required=True)
    SIGNATUREDATE = fields.Date(required=True)

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = [
            'SIGNATUREDATE',
        ]
        in_data = pre_load_date_date_fields(
            in_data,
            date_fields,
            date_format="%d-%b-%Y",
        )
        return in_data
