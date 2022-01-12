from flask import *
from flask_socketio import *
import random
import mysql.connector as mysqli
import json
import datetime
import config
waktu_sekarang=datetime.datetime.now()
app=Flask(__name__)
Socket=SocketIO(app)
app.secret_key="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Connection:
    host=config.HOST
    user=config.USER
    passord=config.PASSWORD
    def __init__(self):
        try:
            self.koneksi=mysqli.connect(host=self.host,user=self.user,password=self.passord,database="dbsimple_chat")
        except:
            self.koneksi=mysqli.connect(host=self.host,user=self.user,password=self.passord)
            kursor=self.koneksi.cursor()
            kursor.execute("CREATE DATABASE {}".format(self.database))
            del(self.koneksi)
            del(kursor)
            self.koneksi=mysqli.connect(host=self.host,user=self.user,password=self.passord,database="dbsimple_chat")
            kursor = self.koneksi.cursor()
            kursor.execute("CREATE TABLE user (id_akun varchar(50) primary key, nama_akun varchar(15))")
            kursor.execute("CREATE TABLE chat (id_chat varchar(3) primary key, id_akun varchar(50), tipe varchar(1), isi_chat longtext, tanggal datetime)")


def gen_random(lim):
    str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    has = ""
    for x in range(lim):
        ind = random.randint(0, (len(str) - 1))
        has = has + str[ind]
    return has
class Model_chat:
    def __init__(self):
        kn=Connection()
        self.koneksi=kn.koneksi
        self.mu=Model_user()
    def gen_random(self,lim):
        str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        has = ""
        for x in range(lim):
            ind = random.randint(0, (len(str) - 1))
            has = has + str[ind]
        return has
    def read_all(self):
        query="SELECT * FROM chat ORDER BY tanggal ASC"
        cursor=self.koneksi.cursor(dictionary=True)
        cursor.execute(query)
        hasil=cursor.fetchall()
        for hs in hasil:
            hasil[hasil.index(hs)]['tanggal']=hs['tanggal'].strftime("%Y-%M-%d %H:%M:%S")
        return hasil
    def insert(self,in_data):
        try:
            in_data['id_chat'] = self.gen_random(5)
            val = (in_data['id_chat'], in_data['id_akun'], in_data['tipe'], in_data['isi_chat'], in_data['tanggal'])
            query = "INSERT INTO chat (id_chat,id_akun,tipe,isi_chat,tanggal) VALUES(%s,%s,%s,%s,%s)"
            cursor = self.koneksi.cursor()
            cursor.execute(query, val)
            self.koneksi.commit()
            return 1
        except:
            return 0

class Model_user:
    def __init__(self):
        kn = Connection()
        self.koneksi = kn.koneksi
    def gen_random(self,lim):
        str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        has = ""
        for x in range(lim):
            ind = random.randint(0, (len(str) - 1))
            has = has + str[ind]
        return has
    def read_all(self):
        query="SELECT * FROM user"
        cursor=self.koneksi.cursor(dictionary=True)
        cursor.execute(query)
        hasil=cursor.fetchall()
        return hasil
    def read_one(self,id_akun):
        query="SELECT * FROM user WHERE id_akun=%s"
        val=(id_akun,)
        cursor=self.koneksi.cursor(dictionary=True)
        cursor.execute(query,val)
        hasil=cursor.fetchall()
        return hasil
    def insert(self,in_data):
        try:
            val = (in_data['id_akun'], in_data['nama_akun'])
            query = "INSERT INTO user (id_akun,nama_akun) VALUES(%s,%s)"
            cursor = self.koneksi.cursor()
            cursor.execute(query, val)
            self.koneksi.commit()
        except:
            return 0
Mc=Model_chat()
Mu=Model_user()
class event_handler:
    def __init__(self,incoming_data):
        self.mc=Model_chat()
        self.mu=Model_user()
        if (incoming_data['data'] == 'initialize'):
            hasil = self.mc.read_all()
            for hs in hasil:
                read_user = self.mu.read_one(hs['id_akun'])
                hasil[hasil.index(hs)]['id_akun'] = read_user[0]['nama_akun']
            nama_user=self.mu.read_one(session['username'])
            emit('initialize',{'data':nama_user[0]['nama_akun']})
            Socket.emit('retrieve_data', {'data': hasil})
        if(incoming_data['data']=='retrieve_data'):
            hasil = self.mc.read_all()
            for hs in hasil:
                read_user = self.mu.read_one(hs['id_akun'])
                hasil[hasil.index(hs)]['id_akun'] = read_user[0]['nama_akun']
            Socket.emit('retrieve_data',{'data':hasil})
        elif(incoming_data['data']=='send_chat'):
            self.insert_chat(incoming_data)
    def insert_chat(self,in_d):
        dt={'id_akun':session['username'],'isi_chat':in_d['chat'],'tipe':'1','tanggal':datetime.datetime.now()}
        cek_user=self.mu.read_one(session['username'])
        if(cek_user[0]['nama_akun']==in_d['token']):
            self.mc.insert(dt)
            hasil=self.mc.read_all()
            for hs in hasil:
                read_user=self.mu.read_one(hs['id_akun'])
                hasil[hasil.index(hs)]['id_akun']=read_user[0]['nama_akun']
            Socket.emit('retrieve_data',{'data':hasil})

def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def index():
    if 'username' in session:
        isi_chat=Mc.read_all()
        return render_template('chat_app/index.html',data=isi_chat)
    else:
        return render_template('login_template/index.html')

def login():
    username = request.form['username']
    token=gen_random(50)
    session['username']=token
    in_data={'id_akun':session['username'],'tipe':'2','tanggal':datetime.datetime.now(),'isi_chat':""}
    in_data_user={'id_akun':token,'nama_akun':username}

    Mc.insert(in_data)
    Mu.insert(in_data_user)
    return redirect(url_for('index'))
def ok(isi):
    print(isi['data'])
app.add_url_rule("/","index",index,methods=['GET'])
app.add_url_rule("/out","logout",logout,methods=['GET'])
app.add_url_rule("/log","login",login,methods=['GET','POST'])
Socket.on_event('ok',ok)
Socket.on_event('request',event_handler)
print("TO ACCESS THE CHAT, TYPE {}:{} ON BROWSER".format(config.IP,config.PORT))
Socket.run(app,host=config.IP,port=config.PORT)