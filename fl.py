__author__ = 'z97'
from flask import Flask
from flask import request
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    r= request;

    hd = request.headers;
    outtxt = str(hd)
    outtxt+="\n"+str(type(request.headers))
    return outtxt

@app.route('/rq',methods=['POST','GET'])
def reflect():
    r=request
    outtxt = '<!DOCTYPE html><html><head lang="en"><meta charset="UTF-8"></head><body>' \
             '<textarea style="width: 100%; height: 1800px">\n'
    outtxt += "your addr:{0}\r\nyour header:\r\n".format(request.remote_addr)
    for k,v in request.headers:
        outtxt+="{0} : '{1}'\r\n".format(k,v)

    outtxt+="\r\nMETHOD = [{0}]!\r\n".format(request.method)
    if request.environ['QUERY_STRING']:
        outtxt+="QUERY_STRING = [{0}]\r\n".format(request.environ['QUERY_STRING'])
    if request.data:
        outtxt+="raw POST data = \r\n"
        outtxt+=request.data.decode()


    outtxt +="\r\n\r\n more information : \r\n"

    env=request.environ
    for k in env:
        outtxt+="{0} : '{1}'\r\n".format(k,env[k])

    outtxt += "</textarea></body></html>"
    fname = GetRqfile_name(request)
    with open(fname,"w") as f:
        f.write(outtxt)

    return outtxt;

@app.route('/srq')
def showrq():
    fname = GetRqfile_name(request)
    outtxt=""
    with open(fname,"r") as f:
        outtxt=f.read()

    return outtxt;

def GetRqfile_name(req):
    ip=req.remote_addr
    fip=ip.replace(".","_")
    rqdir="rq"
    if not os.path.isdir(rqdir):
        os.mkdir(rqdir)
    fullname = "{0}/{1}.rq".format(rqdir,fip)
    return fullname


if __name__ == '__main__':
    app.run()