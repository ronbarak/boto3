import collections
import boto3, botocore
#import csv
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


#def create_spreadsheet(outh_file, spreadsheet_name = "jSonar AWS usage"):
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


def security_groups_worksheet_creation(spread_sheet):
    worksheet = spread_sheet.add_worksheet("security groups", rows=10, cols=6, src_tuple=None, src_worksheet=None, index=None)
    Header = collections.namedtuple('Header', 'cell name bold')
    header_data = dict()
    header_data[1] = Header(cell='A1', name='Name', bold=True)
    header_data[2] = Header(cell='B1', name='Region', bold=True)
    header_data[3] = Header(cell='C1', name='WorksheetCreated: %s' % currentDT, bold=False)
    populate_headers(headers_data=header_data, worksheet=worksheet)
    cells_data = list()

    for r in range(len(REGIONS)):
        region = REGIONS[r]
        region_h = REGIONS_H[r]
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
        #print(list(idle_sg))
        for isg in idle_sg:
            #cells_data.append([list(idle_sg), region_h])
            cells_data.append([isg, region_h])
            print(isg, region_h)
    populate_cells(start_cell='A2', cells_data=cells_data, worksheet=worksheet)


def s3_worksheet_creation(spread_sheet):
    worksheet = spread_sheet.add_worksheet("s3", rows=10, cols=6, src_tuple=None, src_worksheet=None, index=None)
    Header = collections.namedtuple('Header', 'cell name bold')
    header_data = dict()
    header_data[1] = Header(cell='A1', name='Name', bold=True)
    header_data[2] = Header(cell='B1', name='CreationDate', bold=True)
    header_data[3] = Header(cell='C1', name='Region', bold=True)
    header_data[4] = Header(cell='D1', name='WorksheetCreated: %s' % currentDT, bold=False)
    populate_headers(headers_data=header_data, worksheet=worksheet)
   
    cells_data = list()
    for r in range(len(REGIONS)):
        region = REGIONS[r]
        region_h = REGIONS_H[r]
        print()
        print("{} buckets in {}".format("S3", region_h))
        print("---------------------------")
        #client = boto3.client('ec2', region_name=region)
        s3 = boto3.client('s3', region_name=region)
        buckets = s3.list_buckets()
        for i in range(len(buckets['Buckets'])):
            cur = buckets['Buckets'][i]
            print(cur['Name'],"("+str(cur['CreationDate'])+")")
            creation_date = json.dumps(cur['CreationDate'], indent=4, sort_keys=True, default=str)
            cells_data.append([cur['Name'], creation_date, region_h])
    populate_cells(start_cell='A2', cells_data=cells_data, worksheet=worksheet)


def worksheet_creation(spread_sheet, header_data, worksheet_name, worksheet_rows=10, worksheet_cols=8, REGIONS=REGIONS, REGIONS_H=REGIONS_H):
    worksheet = spread_sheet.add_worksheet(worksheet_name, rows=worksheet_rows, cols=worksheet_cols, src_tuple=None, src_worksheet=None, index=None)
    populate_headers(headers_data=header_data, worksheet=worksheet)
    return worksheet


"""
def get_data(debug_header, reg=REGIONS, reg_h=REGIONS_H):   
    cells_data = list()
    for r in range(len(reg)):
        region = reg[r]
        region_h = reg_h[r]
        print()
        print(debug_header)
        #print("Images in {}".format(region_h))
        #print("-----------------------")
        print("-" * len(debug_header)
        ec2 = boto3.resource('ec2', region_name=region)
        images = ec2.images.filter(Owners=['self'])
        for image in images:
            print("[{}] ( {} {} {} {} )".format(image.state, image.id, image.image_type, image.architecture, image.description, image.platform))
            cells_data.append([image.state, image.id, image.image_type, image.architecture, image.description, image.platform, region_h])
    populate_cells(start_cell='A2', cells_data=cells_data, worksheet=worksheet)
"""


def print_debug_headers(r, debug_header, region_h, reg=REGIONS):
    region = reg[r]
    #region_h = reg_h[r]
    print()
    print(debug_header)
    #print("Images in {}".format(region_h))
    #print("-----------------------")
    print("-" * len(debug_header))
    return region
 
def images_worksheet_creation(spread_sheet):
    Header = collections.namedtuple('Header', 'cell name bold')
    header_data = dict()
    cells_data = list()
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
        debug_header = "Images in {}".format(region_h)
        #print_debug_headers(debug_header="Images in {}".format(region_h), reg_h=REGIONS_H, reg=REGIONS)
        region = print_debug_headers(r, debug_header=debug_header, reg=REGIONS, region_h=REGIONS_H)
        """
        region = REGIONS[r]
        region_h = REGIONS_H[r]
        print()
        print("Images in {}".format(region_h))
        print("-----------------------")
        """
        ec2 = boto3.resource('ec2', region_name=region)
        images = ec2.images.filter(Owners=['self'])
        for image in images:
            print("[{}] ( {} {} {} {} )".format(image.state, image.id, image.image_type, image.architecture, image.description, image.platform))
            cells_data.append([image.state, image.id, image.image_type, image.architecture, image.description, image.platform, region_h])
    populate_cells(start_cell='A2', cells_data=cells_data, worksheet=worksheet)


if __name__ == "__main__":
    spread_sheet = create_spreadsheet(spreadsheet_name = "jSonar AWS usage", outh_file = '../client_secret.json')

    images_worksheet_creation(spread_sheet)
    s3_worksheet_creation(spread_sheet)
    security_groups_worksheet_creation(spread_sheet)
    # Delete the default sheet1
    spread_sheet.del_worksheet(spread_sheet.sheet1) 

    #spread_sheet.del_worksheet(spread_sheet.sheet1)
    # share the sheet by email
    spread_sheet.share("rbarak@jsonar.com")
    print()
    print('spread_sheet.share("rbarak@jsonar.com")')
