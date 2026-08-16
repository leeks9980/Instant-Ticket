team = '한화'
Match_X=1
Match_y=1
seat = None
year = None
month = None
day =  None

def update_settings(new_team, new_x, new_y, new_seat, new_year, new_month, new_day):
    global team, Match_X, Match_y, seat, year, month, day
    team, Match_X, Match_y, seat, year, month, day = new_team, new_x, new_y, new_seat, int(new_year), int(new_month),int(new_day)