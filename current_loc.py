import xlrd
from collections import OrderedDict
import simplejson as json


def get_current():
    wb = xlrd.open_workbook(r'C:\Users\Artie\Desktop\current.xls')
    sh = wb.sheet_by_index(0)
    # List to hold dictionaries
    car_list = {}
    coord_list = {}
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        data = OrderedDict()
        coords = OrderedDict()

        row_values = sh.row_values(rownum)
        data['ID'] = row_values[0]
        # data['Car'] = row_values[1]
        data['timestamp'] = row_values[2]
        coords['lat'] = row_values[3]
        coords['lng'] = row_values[4]
        data['Speed'] = row_values[5]
        data['iconImage'] = row_values[6]

        # coord_list = {'coords:': coords}
        data['coords'] = coords

        ctype = row_values[1]
        car_list.setdefault(ctype, [])
        car_list[ctype].append(data)
    #
    j = json.dumps(car_list)
    #
    return j
    #with open('car_current.json', 'w') as f:
    #    f.write(j)

#get_current()