import boto3

#REGION = 'us-west-2'
STATUS = 'running'
REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
region = REGIONS[2]
REGION = region

#rds = boto3.setup_default_session(region_name='us-west-2')

#client = boto3.client('ec2')
#regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
#print(regions)

#for region in REGIONS:
for region in REGION:
	print()
	print("All {0} {1} instances in {2}".format(STATUS, "EC2", region))
	print("--------------------------------------")
	rds = boto3.setup_default_session(region_name=region)
	rds = boto3.client('rds')
	
	ec2 = boto3.resource('ec2')
	
	instances = ec2.instances.filter(
		Filters=[{'Name': 'instance-state-name'}])
		#Filters=[{'Name': 'instance-state-name', 'Values': [STATUS]}])
		#Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	
	for instance in instances:
		for tag in instance.tags:
			print("%s, " % (tag['Value']), end="")
		print("("+instance.id, instance.instance_type+")")


"""
client = boto3.client('ec2')

instances = []
for region in client.describe_regions()['Regions']:
	ec2 = boto3.resource('ec2', region_name=region['RegionName'])
	result = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	for instance in result:																																														
		instances.append(instance.id)
#return instances

print(instances)
"""
