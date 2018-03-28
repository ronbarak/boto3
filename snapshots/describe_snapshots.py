import boto3
from datetime import datetime, timedelta


STATUSES = ('completed', 'pending')
REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("snapshots in {}".format(region_h))
    print("--------------------------")
    rds = boto3.setup_default_session(region_name=region)
    rds = boto3.client('rds')

    ec2 = boto3.resource('ec2')
    for status in STATUSES:
        snapshots = ec2.snapshots.filter(Filters=[{'Name': 'status', 
                                               'Values': [status]}])
        for snapshot in snapshots:
            #print(dir(snapshot))
            print("[%s] " % (status), end="")
            if snapshot.tags:
                for tag in snapshot.tags:
                        print("%s, " % (tag['Value']),end="")
            print("({}, {}, {} {} {})".format(snapshot.id, snapshot.description, snapshot.start_time, snapshot.state, snapshot.owner_id))
        print()
