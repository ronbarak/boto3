from boto3.session import Session

s = Session()
ec2_regions = s.get_available_regions('dynamodb')
dynamodb_regions = s.get_available_regions('dynamodb')
print("ec2_regions:", ec2_regions)
print("dynamodb_regions:", dynamodb_regions)
