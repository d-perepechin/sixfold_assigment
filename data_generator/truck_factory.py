from models.models import TruckLocation, Truck, TruckRoute, Route, Location
import random
import string
from datetime import datetime, timedelta

# class TruckFactory():

def create_truck():
    return Truck(vehicle_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
                 description={'driver': random.choice(['Danila', 'Ivan', 'Anna', 'Sofia']),
                              'random_fact':random.choice(['actually_woman', 'best_boy', 'crazy', 'naked'])
                              }
                 )

def create_route():
    return Route(location_start=Location(lat=random.uniform(30, 80),
                                        lng=random.uniform(10, 40)
                                         ),
                 location_end=Location(lat=59.4369,
                                        lng=24.7535
                                        ),
                 datetime_start=datetime.now(),
                 datetime_end=datetime.now() + timedelta(days=random.randint(5, 30))

    )

def spin_truck():
    tr = TruckRoute(truck=create_truck(), route=create_route())
    datapoints = random.randint(5,1000)
    total_time_seconds = (tr.route.datetime_end - tr.route.datetime_start).days * 86400
    lat_dif = tr.route.location_end.lat - tr.route.location_start.lat
    lng_dif = tr.route.location_end.lng - tr.route.location_start.lng
    for i in range(datapoints):
        seconds_past = (total_time_seconds / datapoints) * i
        lat_past = (lat_dif / datapoints) * i
        lng_past = (lng_dif / datapoints) * i
        time_point = tr.route.datetime_start + timedelta(seconds=seconds_past)
        lat_point = tr.route.location_start.lat + lat_past
        lng_point = tr.route.location_start.lng + lng_past
        yield ( TruckLocation(vehicle_id=tr.truck.vehicle_id,
                      timestamp=time_point,
                      location=Location(lat=lat_point, lng=lng_point),
                      status={'ok': True}),
                tr.truck)



