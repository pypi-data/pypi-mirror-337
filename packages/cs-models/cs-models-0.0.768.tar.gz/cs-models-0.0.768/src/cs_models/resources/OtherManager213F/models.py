from sqlalchemy import Column, Integer, String, Date
from ...database import Base


class Othermanager213FModel(Base):
    __tablename__ = '13fothermanager2'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    SEQUENCENUMBER = Column(Integer, nullable=False)
    CIK = Column(String(10))
    FORM13FFILENUMBER = Column(String(17))
    CRDNUMBER = Column(String(9))
    SECFILENUMBER = Column(String(17))
    NAME = Column(String(150), nullable=False)
