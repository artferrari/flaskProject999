from flask import Flask, render_template, request

import coords as hist
import current_loc
import current_loc as curr

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('Car Tracker.html')


@app.route('/historical')
def historial():
    return hist.get_historical()


@app.route('/current')
def current():
    return current_loc.get_current()


@app.route('/getcoords', methods=['POST'])
def getcoords():
    searchKey=None
    if request.method == "POST":
        print("json", request.get_data())
        #print("json1", request.args.get('searchKey'))
        reqData = request.get_data()
        searchKey = reqData[10:]
        print(searchKey.decode("utf-8"))
        print(type(searchKey.decode("utf-8")))
        coords = hist.searchCoords(searchKey.decode("utf-8"))
        #print(coords)
        return coords


app.run(host='localhost', debug=True)