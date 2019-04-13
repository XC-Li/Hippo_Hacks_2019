import googlemaps
import datetime as dt
from datetime import datetime


class GoogleApi(object):
    """Wrapper functions to use google api
    Possible Error:
    Need SSL module: https://slproweb.com/products/Win32OpenSSL.html"""

    def __init__(self, api_key=None):
        if api_key is None:
            api_key = 'AIzaSyBZHyideq3LOHmk6BScSLA_wIChiVFS8k8'
        self.google_map = googlemaps.Client(key=api_key)

    # @staticmethod
    # def transform_time(string):
    #     t = time.strptime(string, '%b %d %Y %I:%M%p')
    #     tt = int(time.mktime(t))
    #     return tt
    @staticmethod
    def transform_time(combined_time):
        if not isinstance(combined_time, datetime):  # input is not a datetime object
            if len(combined_time.split('-')) != 5:
                raise ValueError('Wrong time format, should be year-month-day-hour-minute')
            year, month, day, hour, minute = combined_time.split('-')
            timestamp = dt.datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp()
        else:  # input is a datetime object
            timestamp = combined_time.timestamp()
        return int(timestamp)

    def travel(self, origin, destination, mode, departure_time=None):
        """
        The direction using transit
        :param origin: Str
        :param destination: Str
        :param mode: Str
        :param departure_time: Str, like 'Apr 13 2019 09:30AM'
        :return: Dict
        """
        if mode not in ['walking', 'transit', 'bicycling']:
            raise ValueError('Mode can only be walking, transit, or bicycling')
        if departure_time is None:
            departure_time = 'now'
        else:
            departure_time = self.transform_time(departure_time)
        direction = self.google_map.directions(origin=origin, destination=destination,
                                               mode=mode, departure_time=departure_time)
        # print(direction)
        result = dict()
        result['steps'] = list()
        result['metro'] = list()
        result['bus'] = list()
        result['walk'] = list()
        assert len(direction) == 1
        first_direction = direction[0]
        assert len(first_direction['legs']) == 1
        first_legs = first_direction['legs'][0]

        result['total_time'] = first_legs['duration']['value']

        for step in first_legs['steps']:
            result['steps'].append({'start': step['start_location'], 'end': step['end_location'],
                                    'html': step['html_instructions'], 'travel_mode': step['travel_mode']})
            if step['html_instructions'].startswith('Metro'):
                metro = step['transit_details']
                result['metro'].append({'start': metro['departure_stop'], 'end': metro['arrival_stop'],
                                        'duration': step['duration']['value']})
            elif step['html_instructions'].startswith('Bus'):
                bus = step['transit_details']
                result['bus'].append({'start': bus['departure_stop'], 'end': bus['arrival_stop'],
                                      'duration': step['duration']['value']})
            else:
                result['walk'].append({'duration': step['duration']['value']})
        return result


if __name__ == '__main__':
    g = GoogleApi()
    g.transit(origin='1900 South Eads Street, Arlington, VA',
              destination='AMC Georgetown 14, 3111 K St NW, Washington, DC 20007')
