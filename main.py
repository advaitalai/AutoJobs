from board_handler import BoardHandler

# Seed database with a few job boards
company_list = ['miro', 'accel', 'meta', 'anar']

# Create a board handler object to populate a board csv file
bh = BoardHandler('db.csv')

# Add all career boards to the board handler file
for company in company_list:
    bh.add_board(company, bh.find_board_url(company))
    
print(bh)