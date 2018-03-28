from boto3.session import Session

session = Session()
print("get_available_regions('ec2'):", session.get_available_regions('ec2'))
print("get_available_partitions():", session.get_available_partitions())
print("get_available_resources():", session.get_available_resources())
print("get_available_services():", session.get_available_services())
print("also get_credentials():", session.get_credentials(), " (see http://boto3.readthedocs.io/en/latest/reference/core/session.html)")
