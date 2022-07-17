from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import hashlib

from database import Base


class Key(Base):
    __tablename__ = "keys"
    key = Column(String, primary_key=True, index=True)