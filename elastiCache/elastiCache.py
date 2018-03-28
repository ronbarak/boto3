import boto3

REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("XXX {} instances in {}".format("RDS", region_h))
    print("------------------------------")

    client = boto3.client('rds', region_name=region)
    #all_instances = client.describe_instances()
    db_instances = client.describe_db_instances()
    print(db_instances)

