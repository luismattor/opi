import csv
import pandas
import numpy

from util import toint
from util import tofloat

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
        m0a2 = toint(record[13])
        m3a5 = toint(record[31])
        m6a11 = toint(record[34])
        m12a14 = toint(record[40])
        m15a17 = toint(record[43])
        m18a24 = toint(record[46])
        m15a49 = toint(record[47])
        m15ym = toint(record[25])
        m18ym = toint(record[28])
        m25ym = m18ym - m18a24
        m50ym = m15ym - m15a49
        m25a49 = m25ym - m50ym
        m60ym = toint(record[50])
        m50a59 = m50ym - m60ym
        promhnv = tofloat(record[55])
        table.append((delegacion, localidad, ageb, p0a2,
            m0a2, m3a5, m6a11, m12a14, m15a17,
            m18a24, m25a49, m15a49, m50a59, m60ym, promhnv))

    columns = ['delegacion', 'localidad', 'ageb', 'p0a2',
            'm0a2', 'm3a5', 'm6a11', 'm12a14', 'm15a17',
            'm18a24', 'm25a49', 'm15a49', 'm50a59', 'm60ym', 'promhnv']
    df = pandas.DataFrame(table, columns=columns)

    # Filter delegacion Alvaro Obregon and total AGEB
    df = df[df.delegacion.str.contains('lvaro obreg')]
    df = df[df.localidad.str.contains('ageb')]
    df = df.drop(['localidad'], 1)
    df = df.drop(['delegacion'], 1)

    return df

def printDistinct(df, col_id):
    distinct = df.iloc[:,col_id].unique()
    print distinct

if __name__ == "__main__":
    
    """
    Estimator 1. Compute number of babies from 0 to 6 months in 2010
    We only have data from people from 0 to 2 years. Assuming uniform
    data for children from 0 to 2, we divide by 4 to get estimation
    """
    df = loadData('../data/resultados_ageb_urbana_09_cpv2010.csv')
    df['bebes1'] = df.p0a2 / 4

    """
    Estimator 2. Estimate number of potential mothers for 2016 (women age 15-49)
    Compare with potential mothers for 2010. Magnitude and sign should tell us 
    wether figure is bigger or lower than 2010
    """
    df['m9a11'] = 3 * df.m6a11 / (11 - 6 + 1)
    df['m9a14'] = df.m9a11 + df.m12a14
    df['m44a49'] = 6 * df.m25a49 / (49 - 25 + 1)
    df['mamas2010'] = df.m15a49
    df['mamas2016'] = df.m9a14 + df.m15a49 - df.m44a49
    df['mdiv'] = df.mamas2016 / df.mamas2010
    df['bebes2'] = df.bebes1 * df.mdiv

    result = df.loc[:,['ageb', 'bebes1', 'bebes2']]
    result.to_csv("../data/ageb.csv", index = False)

    print df
    print result
