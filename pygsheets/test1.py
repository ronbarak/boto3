import pygsheets

gc = pygsheets.authorize()

# Open spreadsheet and then workseet
sh = gc.open('jSonar AWS usage')

# create a new sheet with 50 rows and 60 colums
wks = sh.add_worksheet("new sheet",rows=50,cols=60)

"""
# Open spreadsheet and then workseet
sh = gc.open('my new ssheet')
wks = sh.sheet1

# Update a cell with value (just to let him know values is updated ;) )
wks.update_cell('A1', "Hey yank this numpy array")

# update the sheet with array
wks.update_cells('A2', my_nparray.to_list())

# share the sheet with your friend
sh.share("myFriend@gmail.com")
"""
