import matplotlib.pyplot as plt

from staticmap import StaticMap, CircleMarker

HEATMAP_TITLE = 'Matriz de origen-destino para el sistema Ecobici ' +\
        'de Octubre a Diciembre de 2016'

BIKEDEMAND_TITLE = 'Demanda de bicicletas por periodos de 30 minutos'

TIMESERIES_TITLE = 'Uso de la estacion de Octube a Diciembre de 2016'

STATIONDEMAND_TITLE = 'Entrada y salida de bicicletas'

colors = {0:'#FF0000', 1:'#00FF00', 2:'#0000FF', 3:'#FFFD00'}

def plot_src_dst_matrix(matrix, labels, path):
    """Create source-destination plot, use labels for ticks"""
    n_stations = len(labels)
    plt.figure(1, figsize=(120, 80))
    plt.title(HEATMAP_TITLE)
    plt.xticks(range(n_stations), labels, rotation='vertical')
    plt.yticks(range(n_stations), labels)
    plt.imshow(matrix, interpolation='none')
    plt.colorbar()
    plt.grid(True, which='minor')
    plt.savefig(path, format="png")
    plt.close()

def plot_series(days, serie, fit, path):
    """Plot time serie and its linear fit"""
    plt.figure(1, figsize=(15, 10))
    plt.title(TIMESERIES_TITLE)
    plt.xlabel('dias')
    plt.ylabel('uso')
    plt.plot(days, serie, days, fit)
    plt.savefig(path, format="png")
    plt.close()

def plot_bike_demand(histogram, path):
    """Plot bike demand in periods fo 30 min"""
    labels = ['%02d:%02d' % (int(t / 2), 30 * int(t % 2)) for t in range(48)]
    plt.figure(1, figsize=(30, 20))
    plt.title(BIKEDEMAND_TITLE)
    plt.xticks(range(48), labels, rotation='vertical')
    plt.xlabel('tiempo')
    plt.ylabel('demanda')
    plt.plot(histogram)
    plt.savefig(path, format="png")
    plt.close()

def plot_station_demand(matrix, id2station, path, labels=None):
    """Plot station in and out demand"""
    plt.figure(1, figsize=(30, 30))
    plt.title(STATIONDEMAND_TITLE)
    plt.xlabel('Numero de entradas')
    plt.ylabel('Numero de salidas')
    for i, row in enumerate(matrix):
        x = row[0]
        y = row[1]
        if len(labels):
            plt.scatter(x, y, color=colors[labels[i]], s=50)
        else:
            plt.scatter(x, y, s=50)
        plt.annotate("%s" % id2station[i], (x, y))
    plt.axis('equal')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(path, format="png")
    plt.close()

def plot_kmeans_elbow(inertias, path):
    """Plot elbow plot to choose number of cluster for k means"""
    plt.figure(1, figsize=(30, 20))
    plt.title("k vs loss")
    plt.xlabel('k')
    plt.ylabel('loss')
    x = [a for a,b in inertias]
    y = [b for a,b in inertias]
    plt.plot(x,y)
    plt.savefig(path, format="png")
    plt.close()

def plot_route(route, station2loc, path):
    """Draw map with a start and end marker"""
    m = StaticMap(400, 400)
    start = station2loc[route[0]]
    end = station2loc[route[1]]
    marker1 = CircleMarker((start[1], start[0]), '#00FF00', 12)
    marker2 = CircleMarker((end[1], end[0]), '#FF0000', 12)
    m.add_marker(marker1)
    m.add_marker(marker2)
    image = m.render(zoom=15)
    image.save(path)

def plot_stations(stations, station2loc, path):
    """Draw map with a start and end marker"""
    m = StaticMap(800, 800)
    for station in stations:
        lat = station2loc[station][0]
        lon = station2loc[station][1]
        marker = CircleMarker((lon, lat), '#0000FF', 12)
        m.add_marker(marker)
    image = m.render(zoom=15)
    image.save(path)
