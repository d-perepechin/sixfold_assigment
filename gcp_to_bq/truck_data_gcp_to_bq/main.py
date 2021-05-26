def truck_data_to_bq(event, context):
    import os
    from google.cloud import bigquery


    PROJECT_NAME = 'dataengeneeringbook'
    DATASET_NAME = 'sixfold'
    TABLE_NAME = 'truck_data'
    schema = [
        bigquery.SchemaField('vehicle_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('description', 'STRING', mode='NULLABLE')
    ]

    table_id = f'{PROJECT_NAME}.{DATASET_NAME}.{TABLE_NAME}'
    uri = os.path.join('gs://', event['bucket'], event['name'])

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        ignore_unknown_values=True
    )
    client = bigquery.Client()
    load_job = client.load_table_from_uri(
        uri,
        table_id,
        job_config=job_config
    )
    load_job.result()