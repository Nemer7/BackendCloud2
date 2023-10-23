import sys
import boto3
import os
import mysql.connector

aws_access_key = 'AKIAV5IV5U6P5NEVGDGV'
aws_secret_key = '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'
aws_region = "us-west-2"  
db_instance_identifier = "database-lab"


client = boto3.client("rds", region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

response = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
endpoint = response["DBInstances"][0]["Endpoint"]["Address"]
username = "admin"
password = "admin123"



def connect():

    try: 
        
        conn = mysql.connector.connect(
            host=endpoint,
            user=username,
            password=password,
            database="bdlab"
        )
        return conn   
    except Exception as e:
        print("Database connection failed due to {}".format(e))