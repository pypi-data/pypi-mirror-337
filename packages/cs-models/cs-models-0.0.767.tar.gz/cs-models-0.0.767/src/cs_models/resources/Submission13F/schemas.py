from marshmallow import Schema, fields, pre_load
from ...utils.utils import pre_load_date_date_fields


class Submission13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    FILING_DATE = fields.Date(required=True)
    SUBMISSIONTYPE = fields.String(required=True)
    CIK = fields.String(required=True)
    PERIODOFREPORT = fields.Date(required=True)

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = [
            'FILING_DATE',
            'PERIODOFREPORT',
        ]
        in_data = pre_load_date_date_fields(
            in_data,
            date_fields,
            date_format="%d-%b-%Y",
        )
        return in_data
