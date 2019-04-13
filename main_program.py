import comparison
import google_api
import find_nearest_bike_location
import draw_map
def main_function():
    g = google_api.GoogleApi()
    f = find_nearest_bike_location.FindNearestBikeLocation()
    origin='1900 South Eads Street, Arlington, VA'
    destination='AMC Georgetown 14, 3111 K St NW, Washington, DC 20007'
    departure_time='Apr 13 2019 09:30AM'
    depart, dest = [38.885300, -77.050000], [38.857766, -77.059580]
    # depart = '1900 South Eads Street, Arlington, VA'
    # dest = 'AMC Georgetown 14, 3111 K St NW, Washington, DC 20007'
    result = comparison.comparison(depart, dest, '2019-04-13-09-30')

    # google_route = g.travel(origin=origin,destination=destination,
    #                         mode='transit',departure_time=departure_time)
    x = []
    target_list = []
    for i in result['only_bike'][:-1]:
        x = x + i
    for j in x[:-1]:
        target_list.append(j[0])
    draw_map.draw_map(target_list)