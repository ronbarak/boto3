import boto3

#STATUSES = ( 'available', 'pending' )
REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')

for i in range(len(REGIONS)):
    region = REGIONS[i]
    region_h = REGIONS_H[i]
    print()
    print("Images in {}".format(region_h))
    print("-----------------------")
    rds = boto3.setup_default_session(region_name=region)
    rds = boto3.client('rds')

    ec2 = boto3.resource('ec2')
    images = ec2.images.filter(Owners=['self'])
    for image in images:
        print("[{}] ( {} {} {} {} )".format(image.state, image.id, image.image_type, image.architecture, image.description, image.platform))
