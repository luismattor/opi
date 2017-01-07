import csv
import numpy
import pandas

from datetime import datetime
from util import fix_ms

TEST_SIZE = 5000

dt_fmt_12 = '%d/%m/%Y %I:%M:%S %p'
dt_fmt_11 = '%Y-%m-%d %H:%M:%S'
dt_fmt_09 = '%d/%m/%Y %H:%M:%S'

def loadFile(path, fmt, hasheader=True, delimiter=','):
    csvfile = open(path, 'r')
    records = csv.reader(csvfile, delimiter=delimiter, quotechar='"')

    if hasheader:
        headers = records.next()
        for i, h in enumerate(headers):
            print i, h

    table = []
    count = 0
    for record in records:
        genre = record[0].lower()
        age = int(record[1].lower())
        bike = record[2].lower()

        start_st = record[3].lower()
        start_date = record[4]
        start_time = fix_ms(record[5])
        start_dt = datetime.strptime(start_date + ' ' + start_time, fmt)

        end_st = record[6].lower()
        end_date = record[7]
        end_time = fix_ms(record[8])
        end_dt = datetime.strptime(end_date + ' ' + end_time, fmt)
        table.append((genre, age, bike, start_st, start_dt, end_st, end_dt))
        count += 1
        if count == TEST_SIZE:
            break
    return table

def loadAll():
    # Read 2016-12. Fix padding in Hour
    t1 = loadFile('../data/2016-12.csv', dt_fmt_12, hasheader=True)
    # Read 2016-11. Fix microseconds
    t2 = loadFile('../data/2016-11.csv', dt_fmt_11, hasheader=False)
    # Read 2016-09. Fix padding in hour. Fix microseconds
    t3 = loadFile('../data/2016-09.csv', dt_fmt_09,
            hasheader=True, delimiter=';')
    
    columns = ['genre', 'age', 'bike', 'start_st', 'start_dt',
            'end_st', 'end_dt']
    df = pandas.DataFrame(t1 + t2 + t3, columns=columns)
    return df

if __name__ == "__main__":

    df = loadAll()

    # Promedio de uso:
    df['delta'] = df['end_dt'] - df['start_dt']
    df['time'] = df['start_dt'].apply(lambda x: x.hour)
    print df

    
