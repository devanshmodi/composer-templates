import airflow
from datetime import datetime
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator

dag = DAG(
    dag_id='bq_to_gcs_simple_dag',
    schedule_interval='@once',
    start_date=airflow.utils.dates.days_ago(0)
)

with dag:
    start = DummyOperator( task_id='start')

    bq_query_execute = airflow.providers.google.cloud.operators.bigquery.BigQueryExecuteQueryOperator (
                            task_id = 'bq_query_execute',
                            sql = 'SELECT * FROM `devansh-365318.airflow_demo.covid` WHERE case_reported_date = "2021-08-18"',
                            use_legacy_sql = False,
                            write_disposition = 'WRITE_TRUNCATE',
                            allow_large_results = True,
                            destination_dataset_table = 'devansh-365318.airflow_demo.tmp_covid',
                            trigger_rule='none_failed')

    export_to_gcs = airflow.providers.google.cloud.transfers.bigquery_to_gcs.BigQueryToGCSOperator (
                            task_id = 'export_to_gcs',
                            source_project_dataset_table = 'devansh-365318.airflow_demo.tmp_covid',
                            destination_cloud_storage_uris = 'gs://composer-gcs-to-bq-demo/export_files/covid.csv',
                            export_format = 'CSV',
                            field_delimiter = ',',
                            print_header = True,
                            trigger_rule='none_failed')

    start >> bq_query_execute >> export_to_gcs