from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Summarypage(Base):
    __tablename__ = '13fsummarypage'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    OTHERINCLUDEDMANAGERSCOUNT = Column(Integer)
    TABLEENTRYTOTAL = Column(Integer)
    TABLEVALUETOTAL = Column(Integer)
    ISCONFIDENTIALOMITTED = Column(String(1))
