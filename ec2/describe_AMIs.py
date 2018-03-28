import boto3

STATUSES = ( 'available', 'pending' )
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
    for status in STATUSES:

        images = ec2.images.filter(Owners = ["self"]).all()
        #images = ec2.images.filter()

        for image in images:
            #print("image__dict__:", image.__dict__)
            #print("dir(image):", dir(image))
            print("[{}] ( {} {} {} {} )".format(status, image.id, image.image_type, image.architecture, image.description, image.platform))
        print()
