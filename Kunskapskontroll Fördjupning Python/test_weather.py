import logging
from util.util import to_float, today_date, setup_logger

logger = logging.getLogger("weather")
logger.addHandler(setup_logger("test.log"))

def test_to_float():
    assert to_float("15.5") == 15.5
    assert to_float(20) == 20.0
    assert to_float("abc") is None

# kollar att to float fungerar som den ska och returnerar None vid fel

def test_today_date_format():
    date = today_date()
    assert len(date) == 10
    assert date[4] == "-" and date[7] == "-"

    # kollar att dagens datum är i rätt format YYYY-MM-DD och har längden 10
    # kollar också att det finns bindestreck på rätt plats