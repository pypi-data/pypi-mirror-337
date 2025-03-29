from marshmallow import Schema, fields


class SummarypageSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    OTHERINCLUDEDMANAGERSCOUNT = fields.Integer()
    TABLEENTRYTOTAL = fields.Integer()
    TABLEVALUETOTAL = fields.Integer()
    ISCONFIDENTIALOMITTED = fields.String()
