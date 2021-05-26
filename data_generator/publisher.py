import os
import time
from google.cloud import pubsub_v1
from truck_factory import spin_truck
from config import PROJECT_NAME, TOPIC_TRUCK_LOCATION, TOPIC_TRUCK_DATA, CREDENTIAL_PATH

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

publisher  = pubsub_v1.PublisherClient()
topic_location = publisher.topic_path(PROJECT_NAME, TOPIC_TRUCK_LOCATION)
topic_truck_data = publisher.topic_path(PROJECT_NAME, TOPIC_TRUCK_DATA)

data_counter = 0
for n in range(1, 1000):
    ride = spin_truck()
    while ride:
        try:
            location, truck = next(ride)
            location = location.json().encode("utf-8")
            truck = truck.json().encode("utf-8")
        except StopIteration:
            publisher.publish(topic_truck_data, truck)
            break
        future = publisher.publish(topic_location, location)
        time.sleep(0.1)

        data_counter += 1
        if data_counter % 100 == 0:
            print('data points send ', data_counter)
