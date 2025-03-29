from marshmallow import Schema, fields


class OthermanagerSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    OTHERMANAGER_SK = fields.Integer(required=True)
    CIK = fields.String()
    FORM13FFILENUMBER = fields.String()
    CRDNUMBER = fields.String()
    SECFILENUMBER = fields.String()
    NAME = fields.String(required=True)
