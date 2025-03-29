from marshmallow import Schema, fields


class InfotableSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    INFOTABLE_SK = fields.Integer(required=True)
    NAMEOFISSUER = fields.String(required=True)
    TITLEOFCLASS = fields.String(required=True)
    CUSIP = fields.String(required=True)
    FIGI = fields.String()
    VALUE = fields.Integer(required=True)
    SSHPRNAMT = fields.Integer(required=True)
    SSHPRNAMTTYPE = fields.String(required=True)
    PUTCALL = fields.String()
    INVESTMENTDISCRETION = fields.String(required=True)
    OTHERMANAGER = fields.String()
    VOTING_AUTH_SOLE = fields.Integer(required=True)
    VOTING_AUTH_SHARED = fields.Integer(required=True)
    VOTING_AUTH_NONE = fields.Integer(required=True)
