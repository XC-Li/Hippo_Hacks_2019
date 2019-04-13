import google_api
import datetime as dt
from datetime import datetime
from find_nearest_bike_location import *
g = google_api.GoogleApi()
find_bike = FindNearestBikeLocation()

def add_time(start_time, add_time):
    if not isinstance(start_time, datetime):  # input is not a datetime object
        if len(start_time.split('-')) != 5:
            raise ValueError('Wrong time format, should be year-month-day-hour-minute')
        year, month, day, hour, minute = start_time.split('-')
        start = dt.datetime(int(year), int(month), int(day), int(hour), int(minute))
        end = start + dt.timedelta(seconds=add_time)
    else:
        end = start_time + dt.timedelta(seconds=add_time)
    return end


def time_of_bicycling(depart, dest, depart_time='2019-04-13-09-30'):
    '''
    it's a problem of walking + bicycling + walking
    Args : depart --> (latitude,longitude)
           dest --> (latitude,longitude)
    Return : path, path_walk1, path_bicycle, path_walk2, total_time
    '''

    # bicycling location
    bike_depart, bike_dest, bike_depart_name, bike_dest_name = find_bike.find_neareast_bike_station(depart, dest)

    # walking
    walk_res1 = g.travel(origin=depart,
                         destination=bike_depart[0],
                         mode='walking',
                         departure_time=depart_time)

    depart_time2 = add_time(depart_time, walk_res1['total_time'])
    # bicycle
    bicycle_result = g.travel(origin=bike_depart[0],
                              destination=bike_dest[0],
                              mode='bicycling',
                              departure_time=depart_time2)

    depart_time3 = add_time(depart_time2, bicycle_result['total_time'])

    walk_res2 = g.travel(origin=bike_dest[0],
                         destination=dest,
                         mode='walking',
                         departure_time=depart_time3)
    # bicycle path
    path_bicycle = []
    for i in bicycle_result['steps']:
        tmp_depart = []
        tmp_depart.append(i['start']['lat'])
        tmp_depart.append(i['start']['lng'])

        tmp_dest = []
        tmp_dest.append(i['end']['lat'])
        tmp_dest.append(i['end']['lng'])

        path_bicycle.append([tmp_depart, tmp_dest])
    walk_time = walk_res1['total_time'] + walk_res2['total_time']

    # first walk path
    path_walk1 = []
    for i in walk_res1['steps']:
        tmp_depart = []
        tmp_depart.append(i['start']['lat'])
        tmp_depart.append(i['start']['lng'])

        tmp_dest = []
        tmp_dest.append(i['end']['lat'])
        tmp_dest.append(i['end']['lng'])

        path_walk1.append([tmp_depart, tmp_dest])
        # second walk path
    path_walk2 = []
    for i in walk_res2['steps']:
        tmp_depart = []
        tmp_depart.append(i['start']['lat'])
        tmp_depart.append(i['start']['lng'])

        tmp_dest = []
        tmp_dest.append(i['end']['lat'])
        tmp_dest.append(i['end']['lng'])

        path_walk2.append([tmp_depart, tmp_dest])

        # return path and time
    total_time = 0
    total_time += bicycle_result['total_time'] + walk_time

    path = []
    path += path_walk1 + path_bicycle + path_walk2
    return path_walk1, path_bicycle, path_walk2, total_time


def time_of_googlemap(depart, dest, depart_time='2019-04-13-09-30'):
    '''
    it's a problem of walking + bus(optional) + metro + bus(optional) + walking
    Args : depart --> (latitude,longitude)
           dest --> (latitude,longitude)
           departure time
    Return : path_walk, path_transit, total_time
    '''
    result = g.travel(origin=depart,
                      destination=dest,
                      mode='transit',
                      departure_time=depart_time)
    total_time = result['total_time']
    # path
    path = []

    for i in result['steps']:
        tmp_depart = []
        tmp_depart.append(i['start']['lat'])
        tmp_depart.append(i['start']['lng'])

        tmp_dest = []
        tmp_dest.append(i['end']['lat'])
        tmp_dest.append(i['end']['lng'])

        path.append([tmp_depart, tmp_dest])

    return path, total_time


# a basic version
# walk + bicycle + metro + walk
def walk_bicycle_metro(depart, dest, depart_time='2019-04-13-09-30'):
    '''
    it's a problem of walking + bicycle + metro
    Args : depart --> (latitude,longitude)
           dest --> (latitude,longitude)
    Return : path_walk,path_bicycle,path_metro,total_time
    '''
    bike_depart, bike_dest, bike_depart_name, bike_dest_name = find_bike.find_neareast_bike_station(depart, dest)

    walk_result = g.travel(origin=depart,
                           destination=bike_depart[0],
                           mode='walking',
                           departure_time=depart_time)
    walk_time = walk_result['total_time']
    depart_time2 = add_time(depart_time, walk_time)

    # path walk
    path_walk = []
    for i in walk_result['steps']:
        if i['travel_mode'] == 'WALKING':
            tmp_depart = []
            tmp_depart.append(i['start']['lat'])
            tmp_depart.append(i['start']['lng'])

            tmp_dest = []
            tmp_dest.append(i['end']['lat'])
            tmp_dest.append(i['end']['lng'])

            path_walk.append([tmp_depart, tmp_dest])

    bicycle_result = g.travel(origin=bike_depart[0],
                              destination=bike_dest[0],
                              mode='bicycling',
                              departure_time=depart_time2)

    bicycle_time = bicycle_result['total_time']
    depart_time3 = add_time(depart_time2, bicycle_time)

    # path bicycle
    path_bicycle = []
    for i in bicycle_result['steps']:
        tmp_depart = []
        tmp_depart.append(i['start']['lat'])
        tmp_depart.append(i['start']['lng'])

        tmp_dest = []
        tmp_dest.append(i['end']['lat'])
        tmp_dest.append(i['end']['lng'])

        path_bicycle.append([tmp_depart, tmp_dest])

    metro_walk_result = g.travel(origin=bike_dest[0],
                                 destination=dest,
                                 mode='transit',
                                 departure_time=depart_time3)
    metro_walk_time = metro_walk_result['total_time']
    path_metro = []
    path_walk2 = []
    for i in metro_walk_result['steps']:
        if i['travel_mode'] == 'WALKING':
            tmp_depart = []
            tmp_depart.append(i['start']['lat'])
            tmp_depart.append(i['start']['lng'])

            tmp_dest = []
            tmp_dest.append(i['end']['lat'])
            tmp_dest.append(i['end']['lng'])

            path_walk2.append([tmp_depart, tmp_dest])

        if i['travel_mode'] == 'TRANSIT':
            tmp_depart2 = []
            tmp_depart2.append(i['start']['lat'])
            tmp_depart2.append(i['start']['lng'])

            tmp_dest2 = []
            tmp_dest2.append(i['end']['lat'])
            tmp_dest2.append(i['end']['lng'])

            path_metro.append([tmp_depart2, tmp_dest2])

    total_time = walk_time + bicycle_time + metro_walk_time
    return path_walk, path_bicycle, path_metro, path_walk2, total_time

def comparison(depart, dest, depart_time):
    b_walk, b_bicycle, b_walk2, t1 = time_of_bicycling(depart,dest,depart_time)
    g_path, t2 = time_of_googlemap(depart,dest, depart_time)
    wbm_walk, wbm_bicycle, wbm_metro, wbm_walk2, t3 = walk_bicycle_metro(depart,dest, depart_time)
    min_time = min(t1,t2,t3)
    best = 0
    if t1 == min_time:
        print('best solution: only use bicycle.')
        best = 1
    elif t2 == min_time:
        print('best solution: use google map solution.')
        best = 2
    elif t3 == min_time:
        print('best solution: use both bicycle and metro.')
        best = 3

    return {
        'best': best,
        'only_bike':[b_walk, b_bicycle, b_walk2, t1],
        'use_google':[g_path, t2],
        'bike_metro':[wbm_walk, wbm_bicycle, wbm_metro, wbm_walk2, t3]
    }


if __name__ == '__main__':
    depart, dest = [38.885300, -77.050000], [38.857766, -77.059580]
    print(comparison(depart, dest, '2019-04-13-09-30'))
