def list_to_dict(lat_lng):
    l = list()
    for i in lat_lng:
        my_dict = dict()
        my_dict['lat'] = i[0]
        my_dict['lng'] = i[1]
        l.append(my_dict)
    return ', '.join(map(str, l))

before="""
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Simple Polylines</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

      // This example creates a 2-pixel-wide red polyline showing the path of
      // the first trans-Pacific flight between Oakland, CA, and Brisbane,
      // Australia which was made by Charles Kingsford Smith.

      function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 15,
          center: {lat: 38.9072, lng: -77.0369},
          //mapTypeId: 'terrain'
        });

        var flightPlanCoordinates = ["""

after = """
        ];
        var flightPath = new google.maps.Polyline({
          path: flightPlanCoordinates,
          geodesic: true,
          strokeColor: '#FF0000',
          strokeOpacity: 1.0,
          strokeWeight: 2
        });

        flightPath.setMap(map);
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBZHyideq3LOHmk6BScSLA_wIChiVFS8k8&callback=initMap">
    </script>
  </body>
</html>
"""


def draw_map(geo_list):
    middle = list_to_dict(geo_list)
    with open("map.html", "w") as text_file:
        text_file.write(before + middle + after)

if __name__ == '__main__':
    draw_map([[37.772,-122.214],
    [21.291,-157.821],
    [-18.142,178.431],
    [-27.467,153.027]])
