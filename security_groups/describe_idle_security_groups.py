import boto3

REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("{} idle security groups in {}".format("EC2", region_h))
    print("-----------------------------------------")

    client = boto3.client('ec2', region_name=region)
    all_instances = client.describe_instances()
    all_sg = client.describe_security_groups()

    instance_sg_set = set()
    sg_set = set()

    for reservation in all_instances["Reservations"] :
      for instance in reservation["Instances"]: 
        for sg in instance["SecurityGroups"]:
          instance_sg_set.add(sg["GroupName"]) 
    
    for security_group in all_sg["SecurityGroups"] :
      sg_set.add(security_group ["GroupName"])
    
    idle_sg = sg_set - instance_sg_set
    print(list(idle_sg))
