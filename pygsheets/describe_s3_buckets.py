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

pp = pprint.PrettyPrinter(indent=4)

currentDT = str(datetime.datetime.now())


def create_spreadsheet(outh_file, spreadsheet_name = "jSonar AWS usage"):
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


def s3_worksheet_creation(spread_sheet):
    worksheet = spread_sheet.add_worksheet("s3", rows=100, cols=26, src_tuple=None, src_worksheet=None, index=None)
    Header = collections.namedtuple('Header', 'cell name bold')
    s3_header_data = dict()
    s3_header_data[1] = Header(cell='A1', name='Name', bold=True)
    s3_header_data[2] = Header(cell='B1', name='CreationDate', bold=True)
    s3_header_data[3] = Header(cell='C1', name='Region', bold=True)
    s3_header_data[4] = Header(cell='D1', name='WorksheetCreated: %s' % currentDT, bold=False)
    populate_headers(headers_data=s3_header_data, worksheet=worksheet)
   
    cells_data = list()
    for r in range(len(REGIONS)):
        region = REGIONS[r]
        region_h = REGIONS_H[r]
        print()
        print("{} buckets in {}".format("S3", region_h))
        print("---------------------------")
        s3 = boto3.client('s3', region_name=region)
        buckets = s3.list_buckets()
        for i in range(len(buckets['Buckets'])):
            cur = buckets['Buckets'][i]
            print(cur['Name'],"("+str(cur['CreationDate'])+")")
            creation_date = json.dumps(cur['CreationDate'], indent=4, sort_keys=True, default=str)
            cells_data.append([cur['Name'], creation_date, region_h])
    populate_cells(start_cell='A2', cells_data=cells_data, worksheet=worksheet)
            


if __name__ == "__main__":
    spread_sheet = create_spreadsheet(spreadsheet_name = "jSonar AWS usage", outh_file = '../client_secret.json')
    spread_sheet.link(syncToCloud=False)

    s3_worksheet_creation(spread_sheet)

    # share the sheet by email
    spread_sheet.share("rbarak@jsonar.com")
