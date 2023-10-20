import sys
import boto3
import os
import mysql.connector

aws_access_key = "AKIAXGYRZECKWFDZH56L"
aws_secret_key = "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"
aws_region = "us-east-2"  # Por ejemplo, "us-east-1"
db_instance_identifier = "rds-lab"


client = boto3.client("rds", region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

response = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
endpoint = response["DBInstances"][0]["Endpoint"]["Address"]
username = "admin"
password = "Chepe1224."


def connect():
    try: 
        connection = mysql.connector.connect(
        host=endpoint,
        user=username,
        password=password,
        database="filesdb"
)

        print("Conexion exitosa")
    except Exception as e:
        print("Database connection failed due to {}".format(e))