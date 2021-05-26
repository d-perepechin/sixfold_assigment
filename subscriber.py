import os
from google.cloud import pubsub_v1
from config import CREDENTIAL_PATH, PROJECT_NAME, SUBSCRIBER_TRUCK_LOCATION

credential_path = CREDENTIAL_PATH
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
timeout = 50

project_id = PROJECT_NAME
subscription_id = SUBSCRIBER_TRUCK_LOCATION

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)


with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()