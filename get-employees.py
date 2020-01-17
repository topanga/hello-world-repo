import boto3
import logging
import json

REGION = 'us-east-1'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading function')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

#def function_handler(event, context):
def function_handler():
    # https://medium.com/@rafael.natali/connecting-to-aurora-serverless-via-lambda-1371ca6f5b7a
    # https://miro.medium.com/max/1567/1*qN4k9dlmFzaB9iSEkWVeyw.png
    # https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
    rdsclient = boto3.client('rds-data')
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    rdsresponse = rdsclient.execute_sql(
        awsSecretStoreArn='arn:aws:secretsmanager:us-east-1:672312526406:secret:myauroradb-login-secret-38RGBH', 
        database='myauroradb', 
        dbClusterOrInstanceArn='arn:aws:rds:us-east-1:672312526406:cluster:myauroradb', 
        sqlStatements='USE myauroradb;SELECT * FROM myauroradb.employees;')
    logger.info("SUCCESS: Have rdsresponse")
    # python_obj = json.loads(rdsresponse)
    prettyJsonResponse = json.dumps(rdsresponse, sort_keys=True, indent=4)
    logger.info(prettyJsonResponse)
    print(prettyJsonResponse)
    return respond(None, rdsresponse)

prettyJsonResult = json.dumps(function_handler(), sort_keys=True, indent=4 )
logger.info(prettyJsonResult)
print(prettyJsonResult)