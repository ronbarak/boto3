import boto3  
from datetime import datetime, timedelta  

region = "us-east-1"  
cloudwatch = boto3.client("cloudwatch", region_name=region)  
today = datetime.now() + timedelta(days=1) # today + 1 because we want all of today  
two_weeks = timedelta(days=14)  
start_date = today - two_weeks

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

available_volumes = get_available_volumes()  
candidate_volumes = [  
    volume
    for volume in available_volumes
    if is_candidate(volume.volume_id)
]

print("available_volumes:", available_volumes)
print("candidate_volumes:", candidate_volumes)
###---#### delete the unused volumes
###---#### WARNING -- THIS DELETES DATA
###---###for candidate in candidate_volumes:  
###---###    candidate.delete()
