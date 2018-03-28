import boto3
from datetime import datetime, timedelta


def get_metrics(volume_id):  
    """Get volume idle time on an individual volume over `start_date`
       to today"""
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName='VolumeIdleTime',
        Dimensions=[{'Name': 'VolumeId', 'Value': volume_id}],
        Period=3600,  # every hour
        StartTime=start_date,
        EndTime=today,
        Statistics=['Minimum'],
        Unit='Seconds'
    )
    print("metrics:", metrics)
    return metrics['Datapoints']

def is_candidate(volume_id):  
    """Make sure the volume has not been used in the past two weeks"""
    metrics = get_metrics(volume_id)
    if len(metrics):
        for metric in metrics:
            # idle time is 5 minute interval aggregate so we use
            # 299 seconds to test if we're lower than that
            if metric['Minimum'] < 299:
                return False
    # if the volume had no metrics lower than 299 it's probably not
    # actually being used for anything so we can include it as
    # a candidate for deletion
    return True


STATUSES = ['available', 'in-use']
REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

today = datetime.now() + timedelta(days=1) # today + 1 because we want all of today  
two_weeks = timedelta(days=14)  
start_date = today - two_weeks

for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("{} volumes in {}".format("EC2", region_h))
    print("----------------------------")
    rds = boto3.setup_default_session(region_name=region)
    rds = boto3.client('rds')
    cloudwatch = boto3.client("cloudwatch", region_name=region) 

    ec2 = boto3.resource('ec2')
    for status in STATUSES:
        volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 
                                               'Values': [status]}])
        for volume in volumes:
            print("[%s] " % (status), end="")
            if volume.tags:
                for tag in volume.tags:
                        print("%s, " % (tag['Value']),end="")
            print("({}, {}GB, {})".format(volume.id, volume.size, volume.volume_type))
        print()
