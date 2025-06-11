# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Adresa naší databáze. Pro SQLite je to soubor.
DATABASE_URL = "sqlite:///./app.db"

# Engine je hlavní vstupní bod do databáze.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # Toto je potřeba jen pro SQLite
)

# Session bude instance našeho "rozhovoru" s databází.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base zdědíme z models.py, aby databáze věděla o našich modelech.
Base = declarative_base()