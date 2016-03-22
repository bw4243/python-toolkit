# all the imports
import re

from bs4 import BeautifulSoup
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
    # userinfo.quick_bind_user(request.args['cookie'], request.args['url'])
    userinfo.add_user(request.args['userid'],request.args['nick_name'],request.args['cookie'],request.args['oid_md5'])
    return 'ok'



@app.route('/parse_others')
def parse_others():
    text=request.args['text']
    soup = BeautifulSoup(text, "html.parser")
    nick_name=soup.find_all('h4','my_name',limit=1)[0].get_text()
    userid=soup.find_all('p','my_ID',limit=1)[0].get_text()[3:]
    # result=soup.find(text=re.compile(r"\{openidMD5:'([A-Z0-9a-z]+)'"))

    oid_md5=re.search(r"openidMD5:'([A-Z0-9a-z]+)'",soup.text,re.M|re.I).group(1)


    return nick_name+','+userid+","+oid_md5

if __name__ == '__main__':
    app.run("127.0.0.1",port=8888, debug=True)
