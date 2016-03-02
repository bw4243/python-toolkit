# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import shenhua

from shike import userinfo

# create out little application :)
app = Flask(__name__)
app.config.from_object(__name__)

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


@app.route('/')
def index():
    print("sdf")
    return render_template('shike_reg.html')


@app.route('/shenhua_login')
def shenhua_login():
    return shenhua.login()


@app.route('/get_phones')
def get_phones():
    token=request.args['token']
    shenhua.release_phones(token)
    return shenhua.get_phones(token, int(request.args['num']))


@app.route('/get_msg')
def get_msg():
    return shenhua.get_msg_once(request.args['token'], request.args['phone'])



@app.route('/bind_user')
def bind_user():
    userinfo.quick_bind_user(request.args['cookie'], request.args['url'])
    return 'ok'


if __name__ == '__main__':
    app.run("127.0.0.1",port=9999, debug=True)
