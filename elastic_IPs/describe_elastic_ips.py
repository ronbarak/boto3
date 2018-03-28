import boto3

STATUSES = ['running', 'stopped']
REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("{} elastic IPs in {}".format("EC2", region_h))
    print("--------------------------------")
    ec2 = boto3.resource('ec2', region_name=region)
    client = boto3.client('ec2', region_name=region)
    eIPs = list(ec2.vpc_addresses.all())
    for eIP in eIPs:
        print("[{}] ( {} {} {} {} {} )".format(eIP.public_ip, eIP.private_ip_address, eIP.allocation_id, eIP.instance_id, eIP.network_interface_id, eIP.network_interface_owner_id, eIP.public_ip))

