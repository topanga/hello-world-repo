import json
import boto3

database_name = 'HSA_NONSAN_PROD'
db_cluster_arn = 'arn:aws:rds:ap-southeast-1:499461857546:db:prod-hsaplus-db-2'
query='SELECT (CASE WHEN Status=1 THEN \'OK\' ELSE \'BAD\' END) AS Status FROM dbo.tbAllCustomer_NONSAN_JOBSTATUS WHERE JobRunNo=(SELECT MAX(JobRunNo) FROM dbo.tbAllCustomer_NONSAN_JOBSTATUS)'
rds_client=boto3.client('rds-data')

def execute_statement(sql):
    print('===== Example - Simple query =====')
    response = rds_client.execute_statement(
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=sql
    )
    return response

response = execute_statement(query)
print(response['records'])
