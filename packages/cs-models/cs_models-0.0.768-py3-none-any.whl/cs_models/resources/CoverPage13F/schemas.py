from marshmallow import Schema, fields, pre_load
from ...utils.utils import pre_load_date_date_fields


class Coverpage13FSchema(Schema):
    ACCESSION_NUMBER = fields.String(required=True)
    REPORTCALENDARORQUARTER = fields.Date(required=True)
    ISAMENDMENT = fields.String()
    AMENDMENTNO = fields.Integer()
    AMENDMENTTYPE = fields.String()
    CONFDENIEDEXPIRED = fields.String()
    DATEDENIEDEXPIRED = fields.Date()
    DATEREPORTED = fields.Date()
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

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = [
            'REPORTCALENDARORQUARTER',
            'DATEDENIEDEXPIRED',
            'DATEREPORTED'
        ]
        in_data = pre_load_date_date_fields(
            in_data,
            date_fields,
            date_format="%d-%b-%Y",
        )
        return in_data
