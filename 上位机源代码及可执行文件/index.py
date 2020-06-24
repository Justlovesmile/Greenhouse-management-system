from flask import Flask, render_template, request,session
import pymysql
import time
from datetime import timedelta,datetime
import os
import json
import myserial
import sqlapi

app = Flask(__name__)
#设置session参数
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。
ser=''

@app.route('/',methods=['GET','POST'])
def index():
    #print("Welcome")
    return render_template('index.html')

#检查seesion中是否保存用户名，若有，则说明用户已经登陆，返回用户名
@app.route('/check_session/',methods=['GET','POST'])
def check_session():
    data={}
    ans=sqlapi.select_newelogs(1)
    #print(ans)
    try:
        if session.get('nickname'):
            data["nickname"]=session['nickname']
            data["session"]="true"
            if session.get('ser'):
                data["ser"]=session['ser']
            else:
                data["ser"]="false"
            data["model"]=ans[0][2]
            data["et"]=ans[0][3]
            data["eh"]=ans[0][4]
            data["el"]=ans[0][5]
            data["ep"]=ans[0][6]
            return json.dumps(data)
        else:
            data["session"]="false"
            return json.dumps(data)
    except:
        print("串口未运行！请点击开始监测")

@app.route('/getdata/',methods=['GET','POST'])
def getdata():
    index=request.form.get('Index')
    try:
        ans=dealdata(sqlapi.select_newlogs(index))
        #print(ans)
    except Exception as e:
        print("Get data 失败！")
        #print(e)
    else:
        return json.dumps(ans)

@app.route('/getjson/',methods=['GET','POST'])
def getjson():
    H=int(request.form.get('Hour'))
    beforetime=time.strptime((datetime.now()-timedelta(hours=H)).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
    timestamp=int(time.mktime(beforetime))
    try:
        ans=dealdata(sqlapi.select_logs(timestamp))
        #print(ans)
    except Exception as e:
        print("Get Json 失败！")
        #print(e)
    else:
        return json.dumps(ans)

@app.route('/getejson/',methods=['GET','POST'])
def getejson():
    H=int(request.form.get('Hour'))
    beforetime=time.strptime((datetime.now()-timedelta(hours=H)).strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
    timestamp=int(time.mktime(beforetime))
    try:
        ans=dealedata(sqlapi.select_elogs(timestamp))
        #print(ans)
    except Exception as e:
        print("Get Json 失败！")
        #print(e)
    else:
        return json.dumps(ans)

@app.route('/equip/',methods=['GET','POST'])
def equip():
    return render_template('equip.html')

@app.route('/detail/',methods=['GET','POST'])
def detail():
    return render_template('detail.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    return render_template('login.html')     

@app.route('/login_check/',methods=['GET','POST'])
def login_check():
    nickname=request.form.get('nickname')
    password=request.form.get('password')
    try:
        ans=sqlapi.select_users(nickname,password)
    except Exception as e:
        print("登录失败！")
        #print(e)
    else:
        if(ans==True):
            session['nickname']=nickname
        return json.dumps(ans)

#注销登陆账号时清除session['nickname']
@app.route('/clear_session/',methods=['GET','POST'])
def clear_session():
    if session.get('nickname'):
        session.pop('nickname')
    return json.dumps(True)

@app.route('/stop_serial/',methods=['GET','POST'])
def stop_serial():
    print("停止监测")
    myserial.DClosePort(ser)
    session["ser"]='false'
    return json.dumps(True)

@app.route('/begin_serial/',methods=['GET','POST'])
def begin_serial():
    print("开始监测")
    global ser
    ser=myserial.main()
    session['ser']='true'
    return json.dumps(True)

@app.route('/write_serial/',methods=["GET","POST"])
def turnup_serial():
    text=request.form.get('text')
    global ser
    myserial.DWritePort(ser,text)
    return json.dumps(True)

def dealdata(data):
    ans={
        "time":[],
        "temperature":[],
        "humidity":[],
        "light":[],
        "pressure":[]
    }
    for eachline in data:
        ans["time"].append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(eachline[1]))))
        ans["temperature"].append(eachline[2])
        ans["humidity"].append(eachline[3])
        ans["light"].append(eachline[4])
        ans["pressure"].append(eachline[5])
    return ans

def dealedata(data):
    ans={
        "time":[],
        "model":[],
        "temperature":[],
        "humidity":[],
        "light":[],
        "pressure":[]
    }
    for eachline in data:
        ans["time"].append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(eachline[1]))))
        ans["model"].append(eachline[2])
        ans["temperature"].append(eachline[3])
        ans["humidity"].append(eachline[4])
        ans["light"].append(eachline[5])
        ans["pressure"].append(eachline[6])
    return ans

if __name__ == "__main__":
    sqlapi.check()
    app.run(use_reloader=False)