import requests
import pandas as pd
headers = {'api_key': '5d7494bbde0c411981d3832703734b09'}


class FindNearestBikeLocation(object):
    def __init__(self):
        self.df = self.get_bus_location()

    def get_bus_location(self):
        """
        get all capital bike station location information in DC
        """
        system_regions = requests.get('https://gbfs.capitalbikeshare.com/gbfs/en/system_regions.json')
        station_information = requests.get('https://gbfs.capitalbikeshare.com/gbfs/en/station_information.json')
        # region_dic
        region_dic = {}
        for i in system_regions.json()['data']['regions']:
            region_dic[i['region_id']] = i['name']
        # dataframe
        tmp = []
        for item in station_information.json()['data']['stations']:
            region_id = item['region_id']
            # region_idx.append(region_id)

            if str(region_id) in region_dic.keys():
                region = region_dic[str(region_id)]
            tmp.append([item['station_id'], item['name'], item['lat'], item['lon'], item['region_id'], region])

        df = pd.DataFrame(tmp)
        df.columns = ['station_id', 'name', 'latitude', 'longitude', 'region_idx', 'region']
        return df

    def find_neareast_bike_station(self, depart, dest):
        '''
        Args:   depart --> (latitude,longitude)
                dest --> (latitude,longitude)

        Return: depart_bike_station --> (latitude,longitude)
                dest_bike_station --> (latitude,longitude)
                info_depart --> (station_id of the bike station, name of the bike station)
                info_dest --> (station_id of the destination bike station, name of the destination bike station)
        '''
        df = self.df
        min_depart_dist = 10 ** 9
        coordinate_depart = []
        info_depart = {}
        # departure
        for i in range(df.shape[0]):
            x = df.loc[i, :]['latitude']
            y = df.loc[i, :]['longitude']
            depart_dist = ((x - depart[0]) ** 2 + (y - depart[1]) ** 2) ** 0.5
            if depart_dist < min_depart_dist:
                info_depart['station_id'] = int(df.loc[i, :]['station_id'])
                info_depart['name'] = df.loc[i, :]['name']

                min_depart_dist = depart_dist
                if len(coordinate_depart) == 1:
                    coordinate_depart.pop()
                if len(coordinate_depart) == 0:
                    coordinate_depart.append([depart[0], depart[1]])

        # destination
        min_dest_dist = 10 ** 9
        coordinate_dest = []
        info_dest = {}
        for i in range(df.shape[0]):
            x = df.loc[i, :]['latitude']
            y = df.loc[i, :]['longitude']
            dest_dist = ((x - dest[0]) ** 2 + (y - dest[1]) ** 2) ** 0.5
            if dest_dist < min_dest_dist:
                info_dest['station_id'] = int(df.loc[i, :]['station_id'])
                info_dest['name'] = df.loc[i, :]['name']

                min_dest_dist = dest_dist
                if len(coordinate_dest) == 1:
                    coordinate_dest.pop()
                if len(coordinate_dest) == 0:
                    coordinate_dest.append([dest[0], dest[1]])

        return coordinate_depart, coordinate_dest, info_depart, info_dest



if __name__ == '__main__':
    f = FindNearestBikeLocation()
    depart, dest = [38.885300, -77.050000], [38.857766, -77.059580]
    print(f.find_neareast_bike_station(depart, dest))