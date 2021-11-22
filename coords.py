import xlrd
import pyodbc
from collections import OrderedDict
import simplejson as json

def get_query(sql, *kwargs):
    connectionString = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=test;UID=sa;PWD=Password1!'
    #connectionString = 'DRIVER={SQL Server};SERVER=dfdlmje-general-dbs.database.windows.net;DATABASE=test;UID=Y_apac_srir100;PWD=}hq*e<FKt3pq;6\#'
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    cursor.execute(sql, kwargs)
    return cursor.fetchall()


def get_historical():
    sql = """
        select '1' as id, carCode, timestamp, lat, lng, velocity as speed, 'https://i.ibb.co/k6r7MJZ/truck-icon-100-100.png' as iconImage 

  from [test].[dbo].[testGPS4] order by carCode, timestamp

    """
    historical_data = get_query(sql)
    # wb = xlrd.open_workbook(r'C:\Users\Artie\Desktop\map stuff\test_run.xls')
    # sh = wb.sheet_by_index(0)
    # List to hold dictionaries
    car_list = {}
    # coord_list = {}
    # Iterate through each row in worksheet and fetch values into dict

    for row_values in historical_data:
        data = OrderedDict()
        coords = OrderedDict()
        data['ID'] = row_values[0]
        # data['Car'] = row_values[1]
        data['timestamp'] = row_values[2].isoformat()
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
    #with open('car.json', 'w') as f:
    #    f.write(j)


def searchCoords(searchKey):
    # we should search db with searchKey
    sql = """select '1' as id, carCode, timestamp, lat, lng, velocity as speed, 'https://i.ibb.co/k6r7MJZ/truck-icon-100-100.png' as iconImage from [test].[dbo].[testGPS3] 
             where carCode = LEFT((?), CHARINDEX('&', (?) + '&') - 1)
             or convert(varchar(10), timestamp, 101) = right(replace(?, '%2F','/'), 10)
             order by carCode, timestamp"""
    historical_data = get_query(sql, searchKey, searchKey, searchKey)
    # wb = xlrd.open_workbook(r'C:\Users\Artie\Desktop\map stuff\test_run.xls')
    # sh = wb.sheet_by_index(0)
    # List to hold dictionaries
    car_list = {}
    # coord_list = {}
    # Iterate through each row in worksheet and fetch values into dict

    for row_values in historical_data:
        data = OrderedDict()
        coords = OrderedDict()
        data['ID'] = row_values[0]
        # data['Car'] = row_values[1]
        data['timestamp'] = row_values[2].isoformat()
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
