import comparison
import draw_map
from datetime import datetime as dt


def get_current_time():
    now = dt.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    return '-'.join([year, month, day, hour, minute])

def transform_output(result ,key):
    concated_list = []
    target_list = []
    for i in result['use_google'][:-1]:
        concated_list = concated_list + i
    for j in concated_list:
        target_list.append(j[0])
    return target_list


def main_function(origin, destination, depart_time=None):
    if depart_time is None:
        depart_time = get_current_time()
    result = comparison.comparison(origin, destination, depart_time)
    if result['best'] == 1:
        target_list = transform_output(result, 'only_bike')
    elif result['best'] == 2:
        target_list = transform_output(result, 'use_google')
    else:
        target_list = transform_output(result, 'bike_metro')
    draw_map.draw_map(target_list)


if __name__ == '__main__':
    origin = input('origin?>')
    destination = input('Destination?>')
    depart_time = input('Deaprt Time?(Leave blank for now>')
    if len(depart_time) == 0:
        depart_time = get_current_time()
    main_function(origin, destination, depart_time)
    # main_function('1600 S.Joyce St, Arlington, VA', 'AMC Georgetown 14, 3111 K St NW, Washington, DC 20007')
