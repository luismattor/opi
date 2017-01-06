import csv
import pandas
import numpy

from util import toint

def loadData(path):
    csvfile = open(path, 'r')
    records = csv.reader(csvfile, delimiter=',', quotechar='"')
    headers = records.next()
    for i, h in enumerate(headers):
        print i, h

    table = []
    for record in records:
        delegacion = record[3].lower().strip()
        localidad = record[5].lower().strip()
        ageb = record[6].lower().strip()
        p0a2 = toint(record[11])
        #m08a14 = toint(record[])
        #m15a49 = toint(record[])
        #promhnv = tofloat(record[])
        table.append((delegacion, localidad, ageb, p0a2))

    columns = ['delegacion', 'localidad', 'ageb', 'p0a2']
    df = pandas.DataFrame(table, columns=columns)

    # Filter delegacion Alvaro Obregon and total AGEB
    df = df[df.delegacion.str.contains('lvaro obreg')]
    df = df[df.localidad.str.contains('ageb')]

    printDistinct(df, 0)
    printDistinct(df, 1)
    
    print df
    return df

def printDistinct(df, col_id):
    distinct = df.iloc[:,col_id].unique()
    print distinct

if __name__ == "__main__":
    
    df = loadData('../data/resultados_ageb_urbana_09_cpv2010.csv')
    df['tbebes'] = df.p0a2 / 4
    print df
