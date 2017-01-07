import csv
import numpy
import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm

from datetime import datetime
from util import fix_ms
from sklearn import metrics
from sklearn.cluster import KMeans

TEST_SIZE = 100000000

dt_fmt_12 = '%d/%m/%Y %I:%M:%S %p'
dt_fmt_11 = '%Y-%m-%d %H:%M:%S'
dt_fmt_09 = '%d/%m/%Y %H:%M:%S'

def loadFile(path, fmt, hasheader=True, delimiter=','):
    csvfile = open(path, 'r')
    records = csv.reader(csvfile, delimiter=delimiter, quotechar='"')

    if hasheader:
        headers = records.next()
        #for i, h in enumerate(headers):
        #    print i, h

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
    # TODO CHANGE TO INCLUDE ALL LIST
    df = pandas.DataFrame(t1, columns=columns)
    return df

def question1(df):
    # Promedio de uso:
    df['delta'] = df['end_dt'] - df['start_dt']
    print "Promedio de uso: ", df['delta'].mean()

    # Horarios de mayor afluencia
    t1 = df['start_dt'].groupby(df['start_dt'].map(lambda x: x.hour)).agg(
            ['count'])

    # Estaciones de mayor uso
    t2 = df['start_st'].groupby(df['start_st']).agg(['count']).sort_values(
            by=['count'], ascending=False)

    print t1
    print t2

def question2(df):
    t1 = df[['start_st']].groupby([
        df['start_st'],
        df['start_dt'].map(lambda x: x.month).rename('month'),
        df['start_dt'].map(lambda x: x.day).rename('day')]).agg([
            'count'])
    print t1
    # Build time series for each station
    stations = t1.index.get_level_values('start_st')
    ts = {}
    for station in stations:
        if station not in ts:
            s = t1.loc[station].reset_index()['start_st']['count'].tolist()
            if len(s) > 1:
                ts[station] = s
                #print s

    # OLS for each time serie, keep track of slopes
    slopes = {}
    for k in ts:
        path = '../plots/estacion_%s.png' % k
        serie = ts[k]
        x = range(len(serie))
        X = sm.add_constant(x)
        model = sm.OLS(serie, X).fit()
        #print k, len(serie)
        #print model.params[1]
        slopes[k] = model.params[1]
        #plotSeries(x, ts[k], model.predict(), path)

    # Sort slopes
    inverted_slopes = {v:k for k,v in slopes.items()}
    for s in sorted(inverted_slopes):
        print 'Slope: %f, Station: %s' % (s, inverted_slopes[s])

    return t1

def plotSeries(days, serie, fit, path):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlabel('dias')
    ax.set_ylabel('uso')
    ax.plot(days, serie, days, fit)
    plt.savefig(path, format="png")
    plt.close()

def question3(df):
    # Group by start and end
    table = df[['start_st']].groupby([df['start_st'],
        df['end_st']]).agg('count').add_suffix('_count').rename(
                columns={'start_st_count': 'count'}).reset_index()
   
    station2id = build_stations_map(df)
    id2station = {v:k for k,v in station2id.items()}
    labels = [id2station[k] for k in sorted(id2station)]
    n_stations = len(station2id)

    m = numpy.zeros((n_stations, n_stations))
    for index, row in table.iterrows():
        start = station2id[row['start_st']]
        end = station2id[row['end_st']]
        count = row['count']
        m[start][end] = count

    print m

    fig, ax = plt.subplots(figsize=(45, 30))
    #plt.xticks(range(n_stations), labels)
    ax.set_ylabel('uso')
    plt.imshow(m, cmap=plt.get_cmap('hot'), vmin=0, vmax=1)
    plt.savefig('../plots/heatmap.png', format="png")
    plt.close()

def build_stations_map(df):
    all_starts = df['start_st'].unique().tolist()
    all_ends = df['end_st'].unique().tolist()

    stations_map = {}
    counter = 0
    for station in all_starts + all_ends:
        if station not in stations_map:
            stations_map[station] = counter
            counter += 1

    return stations_map

if __name__ == "__main__":

    df = loadAll()

    print len(df['start_st'].unique().tolist())
    print len(df['end_st'].unique().tolist())

    #question1(df)
    #question2(df)
    question3(df)

    print df[0:10]

    
