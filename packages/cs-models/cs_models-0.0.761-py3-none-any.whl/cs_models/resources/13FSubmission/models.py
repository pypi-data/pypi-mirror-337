from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Submission(Base):
    __tablename__ = '13fsubmission'

    ACCESSION_NUMBER = Column(String(25), primary_key=True)
    FILING_DATE = Column(Date, nullable=False)
    SUBMISSIONTYPE = Column(String(10), nullable=False)
    CIK = Column(String(10), nullable=False)
    PERIODOFREPORT = Column(Date, nullable=False)
