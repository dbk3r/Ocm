from sqlalchemy import Column, String, DateTime, Enum, Text
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class CertStatus(enum.Enum):
    active = "active"
    expired = "expired"
    revoked = "revoked"
    deleted = "deleted"

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(String(64), primary_key=True)
    issuer = Column(String(256))
    cn = Column(String(256))
    valid_until = Column(DateTime)
    status = Column(Enum(CertStatus))
    certificate = Column(Text)
    chain = Column(Text)  # JSON-serialisiertes Array der PEMs
    csr = Column(Text)    # PEM-CSR