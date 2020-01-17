import sys
import logging
import rds_config
import pymysql
import os
import socket

import boto3
import base64
from botocore.exceptions import ClientError

REGION = 'us-east-1'

def getLoginSecret():

    decoded_binary_secret = ''
    
    secret_name = "myauroradb-login-secret"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    
    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        decoded_binary_secret = get_secret_value_response['SecretString']
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return decoded_binary_secret

def socket_program():
    # get the hostname
# host = socket.gethostname()
    socket_host = rds_host
    logger.info("host = " + socket_host) 
# socket_host = 169.254.107.85
    
    socket_port = 3306
# 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((socket_host, socket_port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    socket_conn, socket_address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(socket_address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        socket_data = socket_conn.recv(1024).decode()
        if not socket_data:
            # if data is not received break
            break
        print("from connected user: " + str(socket_data))
        socket_data = input(' -> ')
        socket_conn.send(socket_data.encode())  # send data to the client

    socket_conn.close()  # close the connection

def getSqlData() :
    # rds settings 
    # rds_host = "mysqlforlambdatest.cnj87gimxqi1.us-east-1.rds.amazonaws.com"
    # rds_host = "aws-mysql-db.cnj87gimxqi1.us-east-1.rds.amazonaws.com"
    # db_host='myauroradb.cluster-cnj87gimxqi1.us-east-1.rds.amazonaws.com'
    db_host='database-1.cnj87gimxqi1.us-east-1.rds.amazonaws.com'
    db_port=3306
    db_username = rds_config.db_username
    db_password = rds_config.db_password
    db_name = rds_config.db_name

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #db_ip = socket.gethostbyname(rds_host)

    logger.info(db_name + ", " + db_username + ", " + db_password)

    # socket_program()

    # https://pymysql.readthedocs.io/en/latest/modules/connections.html
    # https://pymysql.readthedocs.io/en/latest/user/examples.html
    # https://pypi.org/project/PyMySQL/
    """
    conn = pymysql.connect(host='myauroradb.cluster-cnj87gimxqi1.us-east-1.rds.amazonaws.com',
                             port='3306',
                             user='adminadmin',
                             password='adminadmin',
                             db='myauroradb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    """
    try:
        # https://medium.com/@rafael.natali/connecting-to-aurora-serverless-via-lambda-1371ca6f5b7a
        # https://miro.medium.com/max/1567/1*qN4k9dlmFzaB9iSEkWVeyw.png
        rdsclient = boto3.client('rds-data')
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
        rdsresponse = rdsclient.execute_sql(
            awsSecretStoreArn='arn:aws:secretsmanager:us-east-1:672312526406:secret:myauroradb-login-secret-38RGBH',
            database='myauroradb',
            dbClusterOrInstanceArn='arn:aws:rds:us-east-1:672312526406:cluster:myauroradb',
            sqlStatements='USE myauroradb;SELECT * FROM myauroradb.employees;'
        )
        logger.info("SUCCESS: Have rdsresponse")
        # print(rdsresponse['records'])
        # conn = pymysql.connect(host=db_host, port=db_port, db=db_name, user=db_username, password=db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, connect_timeout=120)
        """
        with conn.cursor() as cursor:
            # Create a new record
            sql = "SHOW DATABASES"
            cursor.execute(sql)
        """
        return rdsresponse['records']
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
    finally:
        # conn.close()
        logger.info("Done !")
        #sys.exit()

def function_handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    print(getLoginSecret())
    print(getSqlData())
    
    item_count = 0
    """
    with conn.cursor() as cur:
        cur.execute("create table Employee ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
        cur.execute('insert into Employee (EmpID, Name) values(1, "Joe")')
        cur.execute('insert into Employee (EmpID, Name) values(2, "Bob")')
        cur.execute('insert into Employee (EmpID, Name) values(3, "Mary")')
        conn.commit()
        cur.execute("select * from Employee")
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
    conn.commit()
    """
    return "Added %d items from RDS MySQL table" %(item_count)


