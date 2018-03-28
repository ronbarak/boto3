import boto3

STATUSES = ['running', 'stopped']
#STATUS = 'running'
REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

#rds = boto3.setup_default_session(region_name='us-west-2')

#for region in REGIONS:
for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("{} instances in {}".format("EC2", region_h))
    print("------------------------------")
    rds = boto3.setup_default_session(region_name=region)
    rds = boto3.client('rds')

    ec2 = boto3.resource('ec2')
    for status in STATUSES:

        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 
                                                            'Values': [status]}])

        for instance in instances:
            print("[%s] " % (status),end="")
            for tag in instance.tags:
                    print("%s, " % (tag['Value']),end="")
            print("("+instance.id, instance.instance_type+")")
        print()
