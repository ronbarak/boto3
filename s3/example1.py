import pygsheets

#gc = pygsheets.authorize()
client = pygsheets.authorize(outh_file='../client_secret.json', outh_nonlocal=True)
client.list_ssheets(parent_id=None)
spread_sheet = client.create("jSonar AWS usage")
worksheet = spread_sheet.add_worksheet("s3", rows=100, cols=26, src_tuple=None, src_worksheet=None, index=None)
spread_sheet.link(syncToCloud=False)

###---#### Open spreadsheet and then workseet
###---###sh = gc.open('my new ssheet')
wks = spread_sheet.sheet1

# Update a cell with value (just to let him know values is updated ;) )
wks.update_cell('A1', "Hey yank this numpy array")

# update the sheet with array
#wks.update_cells('A2', my_nparray.to_list())

# share the sheet with your friend
spread_sheet.share("rbarak@jsonar.com")
