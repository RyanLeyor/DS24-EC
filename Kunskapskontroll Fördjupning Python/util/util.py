import logging
from datetime import datetime

def setup_logger(logfile="weather.log"):
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    return fh
# Skapa en filehandler för loggning och spara i weather.log

def to_float(temp):
    """Convert string or number to float, or return None if it fails."""
    try:
        return float(temp)
    except Exception:
        return None
# försöka konvertera temp till float, returnera None vid fel. Detta hjälper för att lagra temperatur som float i databasen

def today_date():
    """Return today's date in YYYY-MM-DD format."""
    return datetime.today().strftime("%Y-%m-%d")
# returnera dagens datum i formatet YYYY-MM-DD
