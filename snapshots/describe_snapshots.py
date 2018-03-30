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

    ec2 = boto3.resource('ec2', region_name=region)
    snapshots = ec2.snapshots.filter()
    for snapshot in snapshots:
        print("[{0}] ({1}, {2}, {3} {4} {5} {6})".format(snapshot.state, snapshot.volume_size, snapshot.volume_id, snapshot.id, snapshot.description, snapshot.start_time, snapshot.owner_id,),end="")
        if snapshot.tags:
            for tag in snapshot.tags:
                print(" %s;" % (tag['Value']),end="")
        print()
    print()
