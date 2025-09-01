import sqlite3
import datetime
import logging
import csv
from util.util import setup_logger

logger = logging.getLogger("weather")
logger.setLevel(logging.INFO) # allt från info och uppåt loggas
logger.addHandler(setup_logger())

db = sqlite3.connect("weather.db")
cur = db.cursor()

# För att skapa en tabell om den inte finns
cur.execute("""
CREATE TABLE IF NOT EXISTS Weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temperature REAL,
    date TEXT
)
""")
db.commit()

if __name__ == "__main__":
    logger.info("Starting up...")

    try:
        with open("weather.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                city = row.get("city")
                temp = row.get("temperature")
                date = row.get("date")

                if not city or not temp or not date:
                    logger.warning(f"Missing data in row: {row}")
                    continue


                # kolla om  city och date redan finns
                latest = cur.execute(
                    "SELECT * FROM Weather WHERE city = ? AND date = ?",
                    (city, date)
                ).fetchone()

                if latest:
                    logger.info(f"Data for {city} on {date} already exists. Skipping.")
                    continue

                # försök lägga till datan, vid fel logga en error
                try:
                    cur.execute(
                        """INSERT INTO Weather (city, temperature, date)
                           VALUES (?, ?, ?)""",
                        (city, temp, date)
                    )
                    db.commit()
                    logger.info(f"Inserted data for {city} on {date}.")
                except Exception as e:
                    logger.error("Adding record failed with error message:")
                    logger.error(e)

    except Exception as e:
        logger.error("Error opening CSV file.")
        logger.error(e)

    logger.info("Finished processing weather data.")



