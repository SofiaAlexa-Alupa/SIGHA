from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Time, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, time, date

Base = declarative_base()
engine = create_engine('sqlute:///sigha.db' , echo= True)

