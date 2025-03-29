from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Othermanager(Base):
    __tablename__ = '13fothermanager'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    OTHERMANAGER_SK = Column(Integer, primary_key=True)
    CIK = Column(String(10))
    FORM13FFILENUMBER = Column(String(17))
    CRDNUMBER = Column(String(9))
    SECFILENUMBER = Column(String(17))
    NAME = Column(String(150), nullable=False)
