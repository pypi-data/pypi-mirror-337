from marshmallow import Schema, fields


class Coverpage13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    REPORTCALENDARORQUARTER = fields.Date(required=True, format="%d-%b-%Y")
    ISAMENDMENT = fields.String()
    AMENDMENTNO = fields.Integer()
    AMENDMENTTYPE = fields.String()
    CONFDENIEDEXPIRED = fields.String()
    DATEDENIEDEXPIRED = fields.Date(format="%d-%b-%Y")
    DATEREPORTED = fields.Date(format="%d-%b-%Y")
    REASONFORNONCONFIDENTIALITY = fields.String()
    FILINGMANAGER_NAME = fields.String(required=True)
    FILINGMANAGER_STREET1 = fields.String()
    FILINGMANAGER_STREET2 = fields.String()
    FILINGMANAGER_CITY = fields.String()
    FILINGMANAGER_STATEORCOUNTRY = fields.String()
    FILINGMANAGER_ZIPCODE = fields.String()
    REPORTTYPE = fields.String(required=True)
    FORM13FFILENUMBER = fields.String()
    CRDNUMBER = fields.String()
    SECFILENUMBER = fields.String()
    PROVIDEINFOFORINSTRUCTION5 = fields.String(required=True)
    ADDITIONALINFORMATION = fields.String()

