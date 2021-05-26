from google.cloud import bigquery
import os

from config import CREDENTIAL_PATH, PROJECT_NAME, TABLE_NAME, DATASET_NAME

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

def create_dataset(dataset_name: str, project_name: str) -> None:
    dataset_id = f'{project_name}.{dataset_name}'
    dataset_obj = bigquery.Dataset(dataset_id)
    client = bigquery.Client()
    dataset = client.create_dataset(dataset_obj)

def create_table(table_name: str, dataset_name: str, project_name: str, schema: list) -> None:
    table_id = f'{project_name}.{dataset_name}.{table_name}'
    table_obj = bigquery.Table(table_id, schema)
    table_obj.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="timestamp",
    )
    client = bigquery.Client()
    table = client.create_table(table_obj)


schema = [
    bigquery.SchemaField('vehicle_id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('timestamp', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('status', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('location', 'RECORD', mode='REQUIRED', fields=(bigquery.SchemaField('lat', 'FLOAT64', mode='REQUIRED'),
                                                                        bigquery.SchemaField('lng', 'FLOAT64', mode='REQUIRED')))
]


create_table(TABLE_NAME, DATASET_NAME, PROJECT_NAME, schema)