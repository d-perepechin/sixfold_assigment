# sixfold_assigment
1. Choose the storage/tools/services.
- For incoming data stream handling I've picked pub/sub queue (kafka as open-source alternative). Scalable solution that allows us to handle data as we want. Now it's just one place storage, but later it may be fed to outer vendors (who willing to have raw data) or redistributed to other storage platforms.
- As data comes to queue from outer suppliers it may be ill-formated. For streaming data handling I'm using dataflow (flume/flink). For my usage, it's just conversion status/description fields into string and storing them.
- GCS (HDFS alternative) is used to store raw data from dataflow, as we always like to store raw data to be able to rebuild staged view. 
- BigQuery used as BD, schema on write so fields like status/description stored as just plain strings. I wouldn't use this approach as data is hard to query and eventually, it just inflate our DB. If we can determine which fields from status are needed we may add them in schema directly if later we'll decide to have more fields - it's not a problem raw data stored in GCS and we can rebuild our tables.
ButQuery populated through cloud function which is just copying data from GCS to BQ. Especially having 20GB / 200k msg = 1 msg ~ 100kb

In dataflow 5 minute window is used and GCS->BQ is instant, so data available in 5 minutes after emitting. Here any arbitrary window size may be used even real-time injection to BQ directly (and batching to GCS). 

2 Python dummy produces publish data to pubsub
3 ('vehicle_id', 'STRING', mode='REQUIRED') ('timestamp', 'TIMESTAMP', mode='REQUIRED') ('status', 'STRING', mode='NULLABLE'),('location', 'RECORD', mode='REQUIRED', fields=(('lat', 'FLOAT64', mode='REQUIRED'), ('lng', 'FLOAT64', mode='REQUIRED'))
4 done
5 https://datastudio.google.com/reporting/b29136ff-442a-4f71-9abb-44f4095b7422 
BQ partitioned by timestamp and may have additional partitioning on vehicle_id. With reasonable time range any sql query works instantenius. 

1) Dataflow https://cloud.google.com/dataflow/pricing seems to be the most expensive part of the setup. 2vCPU 15 RAM + data processed. In my test example it's little amaounts but let's count for 20GB/day
2 * $0.069 (streaming vCPU) * 24 + 15 * $0.003557 (RAM) * 24 + 20 * $0.018 (processed data) = 5$/day
2) pubsub first 10 gigabytes of usage are free. Rest $40 per TiB. Depends on regions and message size, but let's round up to 1$/month
3) cloud functions. It's pay per usage 2 functions once in 5 min - pricing is not clear at a glance, but took me 1$ per day.
4) standard storage GCS 0.026 per GB/month. May be turned to cold etc. For 1 year of data 20*365 = $190 per month. Without data moving.
5) BigQuery. Split by Analysis pricing and  Storage pricing. 
Queries first 1 TB per month is free, seems to be legit. 
Storage first 10 GB is free. $0.020 per GB. Again if we would store just bare-bones data it'll be enough.

Worst part. The more managed services used the more depending on G services. For example I wanted to enrich data with geolocation info in dataflow - 5$ per 1k request what will bill painfully. And any other enrichment and data-moving may be costly.

As a final thought. I wouldn't make a service with response time 2 min. It's just unfriendly, OLAP DB's like clickhouse or druid let do it real time.
350$ month seems be reasonable, but 4 CCX31 in hetzner may be rented and open source solutions may be used along with G managed.
