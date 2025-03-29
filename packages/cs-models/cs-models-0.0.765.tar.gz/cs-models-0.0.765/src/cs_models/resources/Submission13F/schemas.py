from marshmallow import Schema, fields


class Submission13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    FILING_DATE = fields.Date(required=True)
    SUBMISSIONTYPE = fields.String(required=True)
    CIK = fields.String(required=True)
    PERIODOFREPORT = fields.Date(required=True)
