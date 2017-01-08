import csv
import numpy
import pandas
import statsmodels.api as sm

from datetime import datetime
from util import fix_ms
from sklearn import metrics
from sklearn.cluster import KMeans
from plotting import plot_bike_demand
from plotting import plot_series
from plotting import plot_src_dst_matrix
from plotting import plot_kmeans_elbow
from plotting import plot_station_demand 

TEST_SIZE = 100000000

dt_fmt_12 = '%d/%m/%Y %I:%M:%S %p'
dt_fmt_11 = '%Y-%m-%d %H:%M:%S'
dt_fmt_09 = '%d/%m/%Y %H:%M:%S'

BIKEDEMAND_PATH = '../plots/demanda_bicis.png'

TIMESERIES_PATH_FMT = '../plots/estacion_%s.png'

HEATMAP_PATH = '../plots/heatmap.png'

KMEANS_ELBOW_PLOT_PATH ='../plots/kmeans-elbow.png'

STATIONDEMAND_PATH = '../plots/demanda_estaciones.png'

TIMESERIES_MIN_POINTS = 20

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

def q1_stats(df):
    # Promedio de uso:
    df['delta'] = df['end_dt'] - df['start_dt']
    print "Promedio de uso: ", df['delta'].mean()
    
    # Horarios de mayor afluencia en intervalos de 30 min
    table = df[['start_dt']].groupby([
        df['start_dt'].map(lambda x: x.hour).rename('hour'),
        df['start_dt'].map(lambda x: x.minute/30).rename('minute')]
        ).agg('count').reset_index()
    histogram = numpy.array([0] * 48)
    for i, row in table.iterrows():
        h = row['hour']
        m = row['minute']
        c = row['start_dt']
        histogram[2*h + m] = c
    
    # Estaciones de mayor uso
    table = df['start_st'].groupby(df['start_st']).agg(['count']).sort_values(
            by=['count'], ascending=False).reset_index()
    top_st = [(r['start_st'], r['count']) for i,r in table.iterrows()][0:10]
    return histogram, top_st


def q2_temporal_analysis(df):
    # Group by start, month, day
    table = df[['start_st']].groupby([
        df['start_st'],
        df['start_dt'].map(lambda x: x.month).rename('month'),
        df['start_dt'].map(lambda x: x.day).rename('day')]).agg(['count'])

    # Build time series for each station
    stations = table.index.get_level_values('start_st')
    ts = {}
    for station in stations:
        if station not in ts:
            s = table.loc[station].reset_index()['start_st']['count'].tolist()
            if len(s) > TIMESERIES_MIN_POINTS:
                ts[station] = s

    # OLS for each time serie, keep track of slopes
    slopes = {}
    predictions = {}
    for k in ts:
        serie = ts[k]
        x = range(len(serie)) # TODO: Check if days are consecutive
        X = sm.add_constant(x)
        model = sm.OLS(serie, X).fit()
        slopes[k] = model.params[1]
        predictions[k] = model.predict()

    return ts, slopes, predictions

def q3_build_src_dst_matrix(df):
    # Group by src and dst
    table = df[['start_st']].groupby([df['start_st'],
        df['end_st']]).agg('count').add_suffix('_count').rename(
                columns={'start_st_count': 'count'}).reset_index()
  
    # Create direct and invert index for stations
    station2id = build_station2id_map(df)
    id2station = {v:k for k,v in station2id.items()}
    n_stations = len(station2id)

    # Build src-distination matrix
    m = numpy.zeros((n_stations, n_stations))
    for index, row in table.iterrows():
        start = station2id[row['start_st']]
        end = station2id[row['end_st']]
        count = row['count']
        m[start][end] = count
    
    return m, id2station

def build_station2id_map(df):
    """Build an index for stations, e.g. {0:station20, 1:station15,...}"""
    all_starts = df['start_st'].unique().tolist()
    all_ends = df['end_st'].unique().tolist()
    stations_map = {}
    counter = 0
    for station in all_starts + all_ends:
        if station not in stations_map:
            stations_map[station] = counter
            counter += 1
    return stations_map

def q4_stations_model(df):
    outs = df['start_st'].groupby(df['start_st']).agg(['count']).reset_index(
            ).rename(columns={'start_st':'st'})
    ins = df['end_st'].groupby(df['end_st']).agg(['count']).reset_index(
            ).rename(columns={'end_st':'st'})
    table = pandas.merge(ins, outs, how='outer', on='st').fillna(0)
    
    # Create direct and invert index for stations
    station2id = build_station2id_map(df)
    id2station = {v:k for k,v in station2id.items()}
    n_stations = len(station2id)
    
    # Build st,ins,outs matrix
    m = numpy.zeros((n_stations, 2))
    for index, row in table.iterrows():
        idx = station2id[row['st']]
        ins = row['count_x']
        outs = row['count_y']
        m[idx][0] = ins
        m[idx][1] = outs

    # Apply k-means, eval several ks
    ks = range(1,20)
    inertias = []
    for k in ks:
        model = KMeans(n_clusters=k, random_state=33).fit(m)
        inertias.append(model.inertia_)
    inertias = zip(ks, inertias)

    labels = KMeans(n_clusters=4, random_state=33).fit_predict(m)

    return  m, id2station, inertias, labels

def q5_explain_stations(df):
    print df

if __name__ == "__main__":

    df = loadAll()

    # Question 1. Horarios y estaciones con mas demanda
    #hist, top_st = q1_stats(df)
    #plot_bike_demand(hist, BIKEDEMAND_PATH)
    #print "Estaciones con mas demanda: ", top_st

    # Question 2. Tendencia de uso
    #ts, slopes, predictions = q2_temporal_analysis(df)
    #for k in ts:
    #    path = TIMESERIES_PATH_FMT % k
    #    pred = predictions[k]
    #    serie = ts[k]
    #    plot_series(range(len(serie)), serie, pred, path)
    #rev_slopes = {v:k for k,v in slopes.items()}
    #down_slopes = [(rev_slopes[k], k) for k in sorted(rev_slopes)[0:10]]
    #up_slopes = [(rev_slopes[k], k) for k in sorted(rev_slopes)[-10:]]
    #for s in sorted(rev_slopes):
    #    print 'Slope: %f, Station: %s' % (s, rev_slopes[s])
    #print up_slopes
    #print down_slopes

    # Question 3. Matriz origen-destino
    #matrix, id2station = q3_build_src_dst_matrix(df)
    #labels = [id2station[k] for k in sorted(id2station)]
    #plot_src_dst_matrix(matrix, labels, HEATMAP_PATH)

    # Question 4. Grouping stations based on usage
    #table_in_out, id2station, inertias, labels = q4_stations_model(df)
    #plot_kmeans_elbow(inertias, KMEANS_ELBOW_PLOT_PATH)
    #plot_station_demand(table_in_out, id2station, STATIONDEMAND_PATH, labels)

    # Question 5. Para algunas estaciones, explicar comportamiento
    res = q5_explain_stations(df)
