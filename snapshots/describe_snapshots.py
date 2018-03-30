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
    #snapshots = ec2.snapshots.filter(Filters=[{'Name': 'status', 
    #                                       'Values': [status]}])
    snapshots = ec2.snapshots.filter()
    for snapshot in snapshots:
        #print(dir(snapshot))
        #print("[%s] " % (status), end="")
        #print("({6}, {5}, {0} {1} {2} {3} {4})".format(snapshot.id, snapshot.description, snapshot.start_time, snapshot.state, snapshot.owner_id, snapshot.volume_id, snapshot.volume_size,))
        #print("[{3}] ({6}, {5}, {0})".format(snapshot.id, snapshot.description, snapshot.start_time, snapshot.state, snapshot.owner_id, snapshot.volume_id, snapshot.volume_size,),end="")
        print("[{0}] ({1}, {2}, {3} {4} {5} {6})".format(snapshot.state, snapshot.volume_size, snapshot.volume_id, snapshot.id, snapshot.description, snapshot.start_time, snapshot.owner_id,),end="")
        # [completed] (snap-095e8beec94defae9, Created by CreateImage(i-0e94b269b648eff8b) for ami-6739a91f from vol-0ee4f2ae7a5ae6ef5, 2018-03-14 17:05:34+00:00 completed 627577395509)
        if snapshot.tags:
            for tag in snapshot.tags:
                    print(" %s;" % (tag['Value']),end="")
        print()
    print()
    """
    for status in STATUSES:
        snapshots = ec2.snapshots.filter(Filters=[{'Name': 'status', 
                                               'Values': [status]}])
        for snapshot in snapshots:
            #print(dir(snapshot))
            #print("[%s] " % (status), end="")
            if snapshot.tags:
                for tag in snapshot.tags:
                        print("%s, " % (tag['Value']),end="")
            #print("({6}, {5}, {0} {1} {2} {3} {4})".format(snapshot.id, snapshot.description, snapshot.start_time, snapshot.state, snapshot.owner_id, snapshot.volume_id, snapshot.volume_size,))
            print("[{3}] ({6}, {5}, {0})".format(snapshot.id, snapshot.description, snapshot.start_time, snapshot.state, snapshot.owner_id, snapshot.volume_id, snapshot.volume_size,))
            # [completed] (snap-095e8beec94defae9, Created by CreateImage(i-0e94b269b648eff8b) for ami-6739a91f from vol-0ee4f2ae7a5ae6ef5, 2018-03-14 17:05:34+00:00 completed 627577395509)
        print()
    """
