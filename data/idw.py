from math import sqrt, fsum
from data import Record

def IDW(record,records=[], N=1):
    wii = 5
    for r in records:
        di = sqrt((r.x-record.x) ** 2 + (r.y-record.y) ** 2)