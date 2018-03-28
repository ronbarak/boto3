import boto3

rds = boto3.setup_default_session(region_name='us-west-2')

ec2 = boto3.client('ec2')
response = ec2.describe_key_pairs()
print(response)
