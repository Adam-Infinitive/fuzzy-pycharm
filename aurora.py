import sys
import boto3
import os

ENDPOINT="matching-db.cluster-cryhkacrgqgz.us-east-1.rds.amazonaws.com"
PORT="5432"
USR="adam.siwiec"
REGION="us-east-1"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='RDSCreds')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)