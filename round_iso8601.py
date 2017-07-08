from dateutil.parser import parse
from datetime import timedelta


def round_b(x, base=5):
    """
    Rounds a number to base X
    """
    return int(base * round(float(x) / base))

def round_iso8601(ts, round_sec=900, iso_format='Z'):
    """
    Args: 
        iso8601 timestamp, rounding_second, iso_format
    Returns:
        iso8601 timestamp rounded to the nearest rouding_seconds
        Formatted with Z(ulu) time to milliseconds if iso_format is 'Z'
    """
    dt = parse(ts)
    secs = dt.microsecond / 1e6 + dt.second + dt.minute * 60. + dt.hour * 3600.
    new_secs = round_b(secs, round_sec)
    
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    dt = dt + timedelta(seconds=new_secs)
    
    ts = dt.isoformat()
    if iso_format == 'Z':
        ts = ts.split('+')[0] + '.000Z'
    return ts

assert round_iso8601('2017-07-07T11:38:20.121Z', 900, 'Z') == '2017-07-07T11:45:00.000Z'
assert round_iso8601('2017-07-07T11:32:20.121Z', 900, 'Z') == '2017-07-07T11:30:00.000Z'
print "Tests passed"
