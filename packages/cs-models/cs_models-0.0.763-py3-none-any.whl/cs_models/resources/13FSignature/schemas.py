from marshmallow import Schema, fields


class SignatureSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    NAME = fields.String(required=True)
    TITLE = fields.String(required=True)
    PHONE = fields.String()
    SIGNATURE = fields.String(required=True)
    CITY = fields.String(required=True)
    STATEORCOUNTRY = fields.String(required=True)
    SIGNATUREDATE = fields.Date(required=True)
