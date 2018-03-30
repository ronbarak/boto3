import collections
import boto3, botocore
import datetime
import json
import numpy as np
from numpy import array
import pprint 
import pygsheets

REGIONS = ('us-west-1', 'us-east-1', 'us-west-2')
REGIONS_H = ('N. California', 'N. Virginia', 'Oregon')
SPREADSHEET_NAME = "jSonar AWS usage"

pp = pprint.PrettyPrinter(indent=4)

currentDT = str(datetime.datetime.now())


def create_spreadsheet(outh_file, spreadsheet_name = SPREADSHEET_NAME):
    client = pygsheets.authorize(outh_file=outh_file, outh_nonlocal=True)
    client.list_ssheets(parent_id=None)
    spread_sheet = client.create(spreadsheet_name)
    return spread_sheet


def populate_headers(headers_data, worksheet):
    h = headers_data
    header = dict()
    for i in range(len(h)):
        col = i + 1
        header[col] = worksheet.cell(h[col].cell)
        header[col].value = h[col].name
        header[col].text_format['bold'] = h[col].bold
        #pp.pprint(header[col])    
        header[col].update()


def populate_cells(start_cell, cells_data, worksheet):
    worksheet.update_cells(start_cell, cells_data)


def worksheet_creation(spread_sheet, header_data, worksheet_name, worksheet_rows=10, worksheet_cols=8, REGIONS=REGIONS, REGIONS_H=REGIONS_H):
    worksheet = spread_sheet.add_worksheet(worksheet_name, rows=worksheet_rows, cols=worksheet_cols, src_tuple=None, src_worksheet=None, index=None)
    populate_headers(headers_data=header_data, worksheet=worksheet)
    return worksheet


def print_debug_headers(r, debug_header, region_h, reg=REGIONS):
    region = reg[r]
    print()
    print(debug_header)
    print("-" * len(debug_header))
    return region

 
def images_worksheet_creation(spread_sheet, Header, header_data, cells_data):
    header_data[1] = Header(cell='A1', name='Image state', bold=True)
    header_data[2] = Header(cell='B1', name='Image ID', bold=True)
    header_data[3] = Header(cell='C1', name='Image type', bold=True)
    header_data[4] = Header(cell='D1', name='Image architecture', bold=True)
    header_data[5] = Header(cell='E1', name='Image description', bold=True)
    header_data[6] = Header(cell='F1', name='Image platform', bold=True)
    header_data[7] = Header(cell='G1', name='Region', bold=True)
    header_data[8] = Header(cell='H1', name='WorksheetCreated: %s' % currentDT, bold=False)
    worksheet = worksheet_creation(spread_sheet, header_data, worksheet_name="AMI", worksheet_rows=10, worksheet_cols=8)

    for r in range(len(REGIONS)):
        region_h = REGIONS_H[r]
        region = print_debug_headers(r, debug_header="Images in {}".format(region_h), reg=REGIONS, region_h=REGIONS_H)
        client = boto3.resource('ec2', region_name=region)
        images = client.images.filter(Owners=['self'])
        for image in images:
            print("[{}] ( {} {} {} {} )".format(image.state, image.id, image.image_type, image.architecture, image.description, image.platform))
            cells_data.append([image.state, image.id, image.image_type, image.architecture, image.description, image.platform, region_h])
    return cells_data, worksheet


def security_groups_worksheet_creation(spread_sheet, Header, header_data, cells_data):
    header_data[1] = Header(cell='A1', name='Name', bold=True)
    header_data[2] = Header(cell='B1', name='Region', bold=True)
    header_data[3] = Header(cell='C1', name='WorksheetCreated: %s' % currentDT, bold=False)
    worksheet = worksheet_creation(spread_sheet, header_data, worksheet_name="security groups", worksheet_rows=10, worksheet_cols=3)

    for r in range(len(REGIONS)):
        region_h = REGIONS_H[r]
        region = print_debug_headers(r, debug_header="{} idle security groups in {}".format("EC2", region_h), reg=REGIONS, region_h=REGIONS_H)

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
        for isg in idle_sg:
            print(isg, region_h)
            cells_data.append([isg, region_h])
    return cells_data, worksheet


def s3_worksheet_creation(spread_sheet, Header, header_data, cells_data):
    header_data[1] = Header(cell='A1', name='Name', bold=True)
    header_data[2] = Header(cell='B1', name='CreationDate', bold=True)
    header_data[3] = Header(cell='C1', name='Region', bold=True)
    header_data[4] = Header(cell='D1', name='WorksheetCreated: %s' % currentDT, bold=False)
    worksheet = worksheet_creation(spread_sheet, header_data, worksheet_name="s3", worksheet_rows=10, worksheet_cols=4)
   
    for r in range(len(REGIONS)):
        region_h = REGIONS_H[r]
        region = print_debug_headers(r, debug_header="{} buckets in {}".format("S3", region_h), reg=REGIONS, region_h=REGIONS_H)
        client = boto3.client('s3', region_name=region)
        buckets = client.list_buckets()
        for i in range(len(buckets['Buckets'])):
            cur = buckets['Buckets'][i]
            print(cur['Name'],"("+str(cur['CreationDate'])+")")
            creation_date = json.dumps(cur['CreationDate'], indent=4, sort_keys=True, default=str)
            cells_data.append([cur['Name'], creation_date, region_h])
    return cells_data, worksheet


def elastic_IP_worksheet_creation(spread_sheet, Header, header_data, cells_data):
    header_data[1] = Header(cell='A1', name='Public IP', bold=True)
    header_data[2] = Header(cell='B1', name='Private IP', bold=True)
    header_data[3] = Header(cell='C1', name='Allocation ID', bold=True)
    header_data[4] = Header(cell='D1', name='Instance ID', bold=True)
    header_data[5] = Header(cell='E1', name='Network interface ID', bold=True)
    header_data[6] = Header(cell='F1', name='Network interface owner ID', bold=True)
    header_data[7] = Header(cell='G1', name='Region', bold=True)
    header_data[8] = Header(cell='I1', name='WorksheetCreated: %s' % currentDT, bold=False)
    worksheet = worksheet_creation(spread_sheet, header_data, worksheet_name="elastic IPs", worksheet_rows=2, worksheet_cols=9)
   
    for r in range(len(REGIONS)):
        region_h = REGIONS_H[r]
        region = print_debug_headers(r, debug_header="{} elastic IPs in {}".format("EC2", region_h), reg=REGIONS, region_h=REGIONS_H)
        ec2 = boto3.resource('ec2', region_name=region)
        eIPs = list(ec2.vpc_addresses.all())
        for eIP in eIPs:
            print("[{}] ( {} {} {} {} {} )".format(eIP.public_ip, eIP.private_ip_address, eIP.allocation_id, eIP.instance_id, eIP.network_interface_id, eIP.network_interface_owner_id))
            cells_data.append([eIP.public_ip, eIP.private_ip_address, eIP.allocation_id, eIP.instance_id, eIP.network_interface_id, eIP.network_interface_owner_id, region_h])
    return cells_data, worksheet


def ec2_worksheet_creation(spread_sheet, Header, header_data, cells_data):
    STATUSES = ['pending', 'running', 'rebooting', 'stopping', 'stopped', 'shutting-down', 'terminated']

    header_data[1] = Header(cell='A1', name='Status', bold=True)
    header_data[2] = Header(cell='B1', name='tags', bold=True)
    header_data[3] = Header(cell='C1', name='ID', bold=True)
    header_data[4] = Header(cell='D1', name='Type', bold=True)
    header_data[5] = Header(cell='E1', name='Region', bold=True)
    header_data[6] = Header(cell='F1', name='WorksheetCreated: %s' % currentDT, bold=False)
    worksheet = worksheet_creation(spread_sheet, header_data, worksheet_name="ec2", worksheet_rows=10, worksheet_cols=6)
   
    for r in range(len(REGIONS)):
        region_h = REGIONS_H[r]
        region = print_debug_headers(r, debug_header="{} instances in {}".format("EC2", region_h), reg=REGIONS, region_h=REGIONS_H)
        client = boto3.client('rds', region_name=region)
        ec2 = boto3.resource('ec2', region_name=region)
        region_record = list()
        for status in STATUSES:
            status_record = list()
            instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 
                                                                'Values': [status]}])

            for instance in instances:
                record = list()
                print("[%s] " % (status),end="")
                record.append(status)
                tags = ""
                for tag in instance.tags:
                    print("%s, " % (tag['Value']),end="")
                    tags += "%s; " % tag['Value']
                record.append(tags)
                print("("+instance.id, instance.instance_type+")")
                record.extend([instance.id, instance.instance_type, region_h])
                status_record.append(record)
            if len(list(instances)):
                print()
                region_record.append(status_record)
        for i in range(len(region_record)):
            cells_data.extend(region_record[i])
    return cells_data, worksheet


def main():
    spread_sheet = create_spreadsheet(spreadsheet_name = "jSonar AWS usage", outh_file = '../client_secret.json')
    Header = collections.namedtuple('Header', 'cell name bold')
    header_data = dict()
    cells_data = list()

    for func in (   ec2_worksheet_creation,
                    elastic_IP_worksheet_creation,
                    images_worksheet_creation, 
                    s3_worksheet_creation, 
                    security_groups_worksheet_creation
                ):
        header_data = dict()
        cells_data = list()
        cells_data, worksheet = func(spread_sheet, Header, header_data, cells_data)
        populate_cells(start_cell='A2', cells_data=cells_data, worksheet=worksheet)
        
    # Delete the default sheet1
    spread_sheet.del_worksheet(spread_sheet.sheet1) 

    # share the sheet by email
    spread_sheet.share("rbarak@jsonar.com")
    print()
    print('sharing spreadsheet with rbarak@jsonar.com')


if __name__ == "__main__":
    main()
