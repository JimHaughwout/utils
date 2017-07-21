#!/usr/bin/python
import csv
import json

"""
CSV I/O. Reads in CSV, converts rows and writes out 
Uses a generator pattern for memory efficiency
"""

INFILE = 'foo.csv'
OUTFILE = 'bar.csv'

def isodate_it(x):
    """
    Excel dumps all date times to CSV in crappy m/d/y H:M format.
    This parses this Excel format into an ISO-8601 datetime in UTC
    """
    try:
        dt, ts = x.split()
        m, d, y = dt.split('/')
        H, M = ts.split(':')
        x_prime = "%s-%s-%s %s:%s:00.000" % (y.zfill(2), m.zfill(2), d.zfill(2), H.zfill(2), M.zfill(2))
        y = datetime.datetime.strptime(x_prime, "%y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%dT%H:%M:%S.000Z")
        return y
    except:
        print_usage_and_exit("Could not convert to ISO date:\n%r\n\n" % x)


def covert(row):
    row['ts'] = isodate_it(row['ts'])
    return row

row_cnt = 1
with open(OUTFILE, 'wb') as target:
    writer = csv.writer(target)
    with open(INFILE, 'r') as source:    
        data = csv.DictReader(source)
        for row in data:
            if row_cnt > 1:
                writer.writerow(row.values())
            else:
                writer.writerow(row.keys())
                writer.writerow(row.values())
            row_cnt += 1
