from flask import Flask, render_template, request

import coords as hist
import current_loc
import current_loc as curr
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        print(auth)
        #import pdb; pdb.set_trace()
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated





app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("Testing123#"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/test')
@auth.login_required
def test():
    return "you are logged in"

@app.route("/")
@auth.login_required
def index():
    return render_template('Car Tracker.html')


@app.route('/historical')
def historial():
    response = hist.get_historical()

    return response


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


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)

#app.run(host='localhost', debug=True)
